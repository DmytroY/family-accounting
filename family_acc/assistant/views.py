from django.shortcuts import render
import logging
import json, os
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from groq import Groq
from .utils import *

logger = logging.getLogger(__name__)

@login_required
def ai_chat_view(request):
    user = request.user
    family = getattr(user.profile, 'family', None)
    logger.debug(f" -- transactions.views.currency_list: Frontend request.user: {user}, family: {family}")

    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request"}, status=400)
    try:
        data = json.loads(request.body)
        conversation_history = data.get("history", [])
        user_query = get_latest_user_message(conversation_history)
        logger.info(f"-- AI chat: user_query = {user_query}")

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        # classify user intent and extract command if exist
        result = classify_intent(client, user_query)
        intent = result.get("intent", "GENERAL")
        action = result.get("action")
        logger.info(f"-- AI chat: intent = {intent} action = {action}")

        # dispatch
        if intent == "DOCUMENTATION":
            resp = handle_documentation(client, conversation_history, user_query)
        elif intent == "DATA":
            try:
                resp = handle_data(client, conversation_history, user_query, user, family)
            except RuntimeError as e:
                return JsonResponse({"reply": str(e)})
        elif intent == "COMMAND":
            resp = handle_command(action)
        else:  # GENERAL or fallback
            resp = handle_general(client, conversation_history)

        return JsonResponse(resp)

    except Exception as e:
        logger.exception("AI Chat Error")
        return JsonResponse({"reply": f"Error: {str(e)}"}, status=500)