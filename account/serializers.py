from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import Serializer
from .models import Account
from rest_framework import serializers


class UserLoginSerializer(Serializer):

    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

    def authenticate(self):
        """
            Returns a user token if the provided credentials are valid
        """
        try:
            user = Account.objects.get(username=self.validated_data['username'])

        except ObjectDoesNotExist:
            try:
                user = Account.objects.get(email=self.validated_data['username'])
            except ObjectDoesNotExist:
                self.error_messages = "Invalid username / email"
                return None

        if user:
            if check_password(self.validated_data['password'], user.password):
                return user
            else:
                self.error_messages = "Invalid Password"
                return None


class UserAccountSerializer(serializers.ModelSerializer):
    """
    For Serializing user account fields attr
    """
    password = serializers.CharField()

    class Meta:
        model = Account
        fields = ["password", "first_name", "last_name", "email", "phone"]


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

