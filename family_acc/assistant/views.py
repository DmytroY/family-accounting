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

@login_required
def ai_chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("---- Data from fromnend JS ---")
            print(f"data: {data}")
            conversation_history = data.get('history', [])
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            messages = [{"role": "system", "content": get_ai_system_prompt()}]
            messages.extend(conversation_history)

            chat_completion = client.chat.completions.create(
                messages=messages,
                model="openai/gpt-oss-120b",
                max_completion_tokens = 150,
                temperature = 0.5
            )
            print("---- Request to AI API ------")
            print(f"messages:{messages}\n")

            print("---- Response of AI ---------")
            usage_dict = chat_completion.usage.model_dump()
            print(json.dumps(usage_dict, indent=4))
            print("-----------------------------\n")

            return JsonResponse({'reply': chat_completion.choices[0].message.content})
               
        except Exception as e:
            print(f"AI Chat Error: {str(e)}") # Log error to server console
            return JsonResponse({'reply': f"Error: {str(e)}"}, status=500)
    return JsonResponse({'reply': "Invalid request"}, status=400)
