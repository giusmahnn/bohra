from rest_framework import serializers
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the Account model.

    Handles serialization and deserialization of Account instances, including
    creation of new users with hashed passwords. The 'id' field is read-only,
    while the 'password' field is write-only for security purposes.

    Fields:
        - id (read-only): Unique identifier for the account.
        - email: Email address of the account.
        - password (write-only): Password for the account.

    Methods:
        - create(validated_data): Creates a new Account instance using the provided
          validated data, ensuring the password is properly hashed.
    """
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "password"
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
    

