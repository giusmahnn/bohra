from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def jwt_tokens(user):
    """
    Generates JWT refresh and access tokens for a given user.
    Args:
        user (User): The user instance for whom the tokens are to be generated.
    Returns:
        dict: A dictionary containing the 'refresh' and 'access' tokens as strings.
    """

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }



def send_email(user_email, subject, template):
    """
    Sends an HTML email to a specified user.
    Args:
        user_email (str): The recipient's email address.
        subject (str): The subject line of the email.
        template (str): The HTML content to be used as the email body.
    Returns:
        str: A message indicating whether the email was sent successfully or if it failed.
    Raises:
        Exception: If sending the email fails, the exception is caught and a failure message is returned.
    """
    subject = subject
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    email = EmailMultiAlternatives(
        subject=subject,
        body="Email Content",
        from_email=from_email,
        to= to_email
    )
    email.content_subtype = "html"
    email.attach_alternative(template, "text/html")

    try:
        email.send(fail_silently=False)
    except Exception as e:
        print(f"Failed to send email to {user_email}: {str(e)}")
        return "Couldn't send email"
    
    return f"Email successfully sent to {user_email}"