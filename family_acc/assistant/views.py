from django.shortcuts import render

import json, os
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from groq import Groq
from .utils import generate_ai_system_prompt, retrieve_documentation_context, classify_intent

_CACHED_AI_SYSTEM_PROMPT = None

def get_ai_system_prompt():
    global _CACHED_AI_SYSTEM_PROMPT
    if _CACHED_AI_SYSTEM_PROMPT is None:
        # This will only execute once, on the very first chat request
        _CACHED_AI_SYSTEM_PROMPT = generate_ai_system_prompt()
    return _CACHED_AI_SYSTEM_PROMPT

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

            # classify user intent and extract command if exist
            result = classify_intent(client, user_query)
            intent = result.get("intent", "GENERAL")
            action = result.get("action")
            print(f"--- DY --- intent is {intent}")
            print(f"--- DY --- Action is {action}")

            # process user query accordingly to intent
            if intent == "DOCUMENTATION":
                rag_context = retrieve_documentation_context(user_query, top_k=3)
                doc_system_prompt = (
                    "You are an expert assistant for the Family Accounting application. "
                    "Use ONLY the following retrieved documentation to answer the user's question. "
                    "If the answer cannot be found in the context, clearly state that you don't know.\n\n"
                    f"DOCUMENTATION CONTEXT:\n{rag_context}"
                )
                messages = [{"role": "system", "content": doc_system_prompt}]
                messages.extend(conversation_history)
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="openai/gpt-oss-120b",
                    max_completion_tokens=250,
                    temperature=0.3  # Lower temperature for higher factual grounding
                )
                return JsonResponse({'reply': chat_completion.choices[0].message.content})

            if intent == "DATA":
                # request to SQL
                return JsonResponse({'reply': "I will search in database"})

            if intent == "COMMAND":
                if action == "CLEAR_HISTORY":
                    return JsonResponse({
                        'reply': "Chat history cleared.",
                        'action': "CLEAR_HISTORY"  # Frontend JS reads this to clear UI state
                    })

                elif action == "SUMMARIZE_CHAT":
                    # Generate summary using fast model over history
                    summary_prompt = [
                        {"role": "system", "content": "Summarize the key points of this conversation in concise bullet points."}
                    ] + conversation_history[:-1] # Exclude command trigger message

                    summary_res = client.chat.completions.create(
                        messages=summary_prompt,
                        model="openai/gpt-oss-20b",
                        max_completion_tokens=150
                    )
                    return JsonResponse({'reply': summary_res.choices[0].message.content})

                else:
                    return JsonResponse({'reply': "I recognized a command request, but I am unable to perform that action."})

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
