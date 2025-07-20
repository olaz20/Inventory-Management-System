from ..models import User
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email_or_username = data.get("email_or_username")
        password = data.get("password")
        try:
            if "@" in email_or_username:
                user = User.objects.get(email=email_or_username)
            else:
                user = User.objects.get(username=email_or_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email/username or password.")
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email, or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        return user
