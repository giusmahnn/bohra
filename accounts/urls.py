from django.urls import path
from accounts.views import AccountRegistrationView, AccountLoginView, PublicView



urlpatterns = [
    path("api/v1/signup/", AccountRegistrationView.as_view()),
    path("api/v1/login/", AccountLoginView.as_view()),
    path("api/v1/public/", PublicView.as_view())
]