import json, os

from django.shortcuts import render
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

def home(request):
    return render(request, "home.html")

def test(request):

    context = {'hello': _("Hello")}
    return render(request, "test.html", context)

@login_required
def ai_chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            system_prompt = get_ai_system_prompt()
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                model="openai/gpt-oss-120b"
            )
            return JsonResponse({'reply': chat_completion.choices[0].message.content})
        except Exception as e:
            return JsonResponse({'reply': f"Error: {str(e)}"}, status=500)
    return JsonResponse({'reply': "Invalid request"}, status=400)