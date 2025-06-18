from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import AccountSerializer
from accounts.utils import jwt_tokens
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
            return Response({
                "message": "User created successfully",
                "user": serializer.data,
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)