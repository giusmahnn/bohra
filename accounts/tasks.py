from celery import shared_task
from accounts.utils import send_email
from django.conf import settings




@shared_task
def send_welcome_email_task(user_email, subject, template):
    """
        Asynchronous task to send a welcome email to a user.

        Args:
            user_email (str): The recipient's email address.
            subject (str): The subject line of the email.
            template (str): The email template or message body to be sent.

        Returns:
            None

        This task delegates the actual sending of the email to the `send_email` function.
    """
    send_email(user_email, subject, template)