from celery import shared_task
from accounts.utils import send_email
from django.conf import settings




@shared_task
def send_welcome_email_task(user_email, subject, template):
    send_email(user_email, subject, template)