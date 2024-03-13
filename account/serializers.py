import os

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import Serializer
from account.models import Account, OTP
from rest_framework import serializers


class UserLoginSerializer(Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

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
    profile_img = serializers.FileField(required=False)

    class Meta:
        model = Account
        fields = ["password", "first_name", "last_name", "email", "phone", "profile_img"]


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class VerifyOtpSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    signed_user = None

    def is_valid(self, *, raise_exception=False):
        """
        Extends the super class is_valid() by also checking the validity of
        the otp
        """
        super().is_valid()

        try:
            otp_obj = OTP.objects.get(pk=self.validated_data["code"])

            self.signed_user = otp_obj.user

            if otp_obj:
                if otp_obj.is_valid(self.validated_data["code"]):
                    return True
                else:
                    self.error_messages = "expired otp"
            else:
                self.error_messages = "invalid otp"

        except ObjectDoesNotExist:
            self.error_messages = "expired otp"
        return False



class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


