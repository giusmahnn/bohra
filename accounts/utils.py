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