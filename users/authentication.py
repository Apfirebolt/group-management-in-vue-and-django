from django.contrib.auth.backends import BaseBackend
from users.models import CustomUser

class EmailLoginBackend(BaseBackend):
    """
    Custom backend for passwordless authentication with email verification.
    """

    def authenticate(self, request, email=None):
        allowed_emails = ['aspper20@gmail.com']  # Replace with your list
        if email in allowed_emails:
            try:
                user = CustomUser.objects.get(email=email)
                return user
            except CustomUser.DoesNotExist:
                pass
        return None