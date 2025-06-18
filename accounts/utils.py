from rest_framework_simplejwt.tokens import RefreshToken



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