import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from core.models import TelegramUser
# Create your views here.



class TelegramWebhook(APIView):
    """
    APIView to handle Telegram webhook updates.
    Methods
    -------
    post(request, *args, **kwargs):
        Handles incoming POST requests from Telegram webhook.
        - Extracts message and user information from the request.
        - If the message text is '/start', updates or creates a TelegramUser entry.
        - Sends a confirmation message back to the user via Telegram bot.
        - Returns a JSON response indicating success.
    send_bot_message(chat_id, text):
        Sends a message to a Telegram user using the Telegram Bot API.
        - chat_id: Telegram user or chat ID to send the message to.
        - text: The message text to send.
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        message = data.get("message", {})
        text = message.get("text", "")
        user = message.get("from", {})

        if text == "/start":
            TelegramUser.objects.update_or_create(
                telegram_id=user.get("id"),
                defaults={
                    'username': user.get('username'),
                    'first_name': user.get('first_name'),
                    'last_name': user.get('last_name'),
                }
            )

            reply_text = "Hello, your username has been saved!"
            self.send_bot_message(user.get("id"), reply_text)
        return Response({"ok": True}, status=status.HTTP_200_OK)
    

    def send_bot_message(self, chat_id, text):
        url = f"{settings.TELEGRAM_URL}/bot{settings.BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
        }
        requests.post(url, json=payload)