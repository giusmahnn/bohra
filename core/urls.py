from django.urls import path
from core.views import TelegramWebhook


urlpatterns = [
    path("chat-bot/", TelegramWebhook.as_view())
]