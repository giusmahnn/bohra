from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import AccountSerializer, LoginSerializer
from django.template.loader import render_to_string
from accounts.utils import jwt_tokens
from accounts.models import Account
from accounts.tasks import send_welcome_email_task
from django.contrib.auth.hashers import check_password
# Create your views here.



class AccountRegistrationView(APIView):
    """
    API view for registering a new user account.

    POST:
        Registers a new user with the provided data.
        - Expects user registration data in the request body.
        - Validates the data using AccountSerializer.
        - On success, creates the user, generates JWT tokens, and returns a success message along with user data and tokens.
        - On failure, returns validation errors.

    Permissions:
        - AllowAny: No authentication required to access this endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = jwt_tokens(user)
            welcome_template = render_to_string(
                "accounts/welcome_template.html",
                {"user": user}
            )
            send_welcome_email_task.delay(user.email, "Welcome to our platform", welcome_template)
            return Response({
                "message": "User created successfully",
                "user": serializer.data,
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AccountLoginView(APIView):
    """
    API view for handling user login.
    POST:
        Authenticates a user using email and password.
        - Expects: JSON body with 'email' and 'password'.
        - Validates credentials:
            - If the email does not exist, returns 404 with an error message.
            - If the password is incorrect, returns 401 with an error message.
            - If credentials are valid, returns 200 with a welcome message and JWT token.
        - On serializer validation failure, returns 400 with error details.
    Permissions:
        - AllowAny: No authentication required to access this endpoint.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            if email:
                try:
                    user = Account.objects.get(email=email)
                except Account.DoesNotExist:
                    return Response({"error": "User not found with this email."}, status=status.HTTP_404_NOT_FOUND)
                
            if not check_password(password, user.password):
                return Response({"error": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
            
            token = jwt_tokens(user)

            return Response({
                "Message": f"Welcome {email}",
                "Token": token
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PublicView(APIView):
    """
    A public API view that allows unrestricted access.

    This view handles GET requests and returns a simple JSON response indicating that the endpoint is public.

    Methods
    -------
    get(request):
        Handles GET requests and returns a message indicating the endpoint is public.

    Permissions
    -----------
    AllowAny: No authentication or authorization is required to access this endpoint.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            "Message": "This is a Public Endpoint"
        }, status=status.HTTP_200_OK)
    


class ProtectedView(APIView):
    """
    A view that allows access only to authenticated users.

    GET:
        Returns a message indicating that the user is authenticated.

    Permissions:
        - IsAuthenticated: Only authenticated users can access this view.

    Responses:
        200 OK: Returns a JSON object with a message confirming authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "Message": "You are seeing this because you are authenticated"
        }, status=status.HTTP_200_OK)