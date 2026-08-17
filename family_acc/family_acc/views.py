import json, os

from django.shortcuts import render
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from groq import Groq

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
            system_prompt = (
                "You are a helpful financial assistant for a family accounting app. "
                "The app uses a Star-scheme database. The 'Transaction' table stores records "
                "where income is positive and expenses are negative. Dimension tables include "
                "User, Currency, Account, and Category."
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                model="llama-3.3-70b-versatile"
            )
            return JsonResponse({'reply': chat_completion.choices[0].message.content})
        except Exception as e:
            return JsonResponse({'reply': f"Error: {str(e)}"}, status=500)
    return JsonResponse({'reply': "Invalid request"}, status=400)