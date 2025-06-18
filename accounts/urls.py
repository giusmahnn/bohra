from django.urls import path
from accounts.views import AccountRegistrationView



urlpatterns = [
    path("signup/", AccountRegistrationView.as_view()),
]