from django.shortcuts import render

import json, os
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from groq import Groq

_CACHED_AI_SYSTEM_PROMPT = None

def get_ai_system_prompt():
    global _CACHED_AI_SYSTEM_PROMPT
    if _CACHED_AI_SYSTEM_PROMPT is None:
        # This will only execute once, on the very first chat request
        from .utils import generate_ai_system_prompt
        _CACHED_AI_SYSTEM_PROMPT = generate_ai_system_prompt()
    return _CACHED_AI_SYSTEM_PROMPT

def clasify_intent(client: Groq, user_query: str) -> str:
    """Classifies user query into GENERAL, DOCUMENTATION, or DATA"""
    classifier_prompt = (
        "Analyze the user message and classify it into exactly one category:\n"
        "1. GENERAL: Greetings, small talk, general financial advice.\n"
        "2. DOCUMENTATION: Questions about how to use the app, UI, navigation, or API specs.\n"
        "3. USER_DATA: Questions about specific account balances, transactions, spending, or income.\n\n"
        'Respond ONLY with a valid JSON object in this format: {"intent": "GENERAL" | "DOCUMENTATION" | "USER_DATA"}'
    )
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": classifier_prompt},
                {"role": "user", "content": user_query}
            ],
            model="openai/gpt-oss-20b",
            response_format={"type": "json_object"},
            temperature=0.0
        )
        res_data = json.loads(response.choices[0].message.content)
        return res_data.get("intent", "GENERAL")
    except Exception:
        return "GENERAL"  # Fallback to general handling on error

@login_required
def ai_chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # frontend JS data
            conversation_history = data.get('history', [])
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

            # latest user message
            user_query = ""
            if conversation_history:
                latest_msg = conversation_history[-1]
                if latest_msg.get('role') == 'user':
                    user_query = latest_msg.get('content', '')

            # clasify user intent
            intent = clasify_intent(client, user_query) if user_query else "GENERAL"

            # process user query accordingly to intent
            if intent == "DOCUMENTATION":
                # RAG grounded to documentation
                return JsonResponse({'reply': "I will search in documentation"})

            if intent == "USER_DATA":
                # request to SQL
                return JsonResponse({'reply': "I will search in database"})

            # default genearal conversation
            messages = [{"role": "system", "content": get_ai_system_prompt()}]
            messages.extend(conversation_history)

            chat_completion = client.chat.completions.create(
                messages=messages,
                model="openai/gpt-oss-120b",
                max_completion_tokens = 150,
                temperature = 0.5
            )

            return JsonResponse({'reply': chat_completion.choices[0].message.content})
               
        except Exception as e:
            print(f"AI Chat Error: {str(e)}") # Log error to server console
            return JsonResponse({'reply': f"Error: {str(e)}"}, status=500)
    return JsonResponse({'reply': "Invalid request"}, status=400)
