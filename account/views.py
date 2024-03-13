from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework.authtoken.models import Token
from django.db.utils import IntegrityError
from account.models import Account, OTP
from account.serializers import UserLoginSerializer, PasswordChangeSerializer, PasswordResetSerializer, \
    VerifyOtpSerializer

from assets.emails.mail import send_email
from assets.emails.email_messages import PASSWORD_RESET_MESSAGE, USERNAME_REQUEST_MESSAGE
from farmci import settings


class UserLoginView(APIView):
    """
    Logs in a user profile

    Returns: authentication token
    """
    serializer_class = UserLoginSerializer

    def post(self, requests):
        serializer = UserLoginSerializer(data=requests.data)
        if serializer.is_valid():
            user = serializer.authenticate()
            if user:
                # Return the authentication token if credentials is valid
                auth_token, created = Token.objects.get_or_create(user=user)

                return Response({"success": True, "responseMessage": "login success", "token": auth_token.key})

            else:
                return Response({'success': False, "responseMessage": serializer.error_messages}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error_messages": serializer.errors}, status=status.HTTP_404_NOT_FOUND)


class ResetUserPassword(APIView):
    serializer_class = PasswordResetSerializer

    @staticmethod
    def post(request):
        expiry = None
        serializer = PasswordResetSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "responseMessage": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Account.objects.get(email=request.POST['email'])
            password = serializer.validated_data['password']
            otp = OTP(user=user)
            key = otp.create(password)
            try:
                otp.save()
            except IntegrityError:
                # Delete the previous otp and create another
                x = OTP.objects.get(user=user)
                x.delete()
                otp = OTP(user=user)
                key = otp.create(password)
                otp.save()

            send_email(
                recipient_email=user.email,
                subject="Password Reset",
                message=PASSWORD_RESET_MESSAGE.format(
                    full_name=user.get_full_name().title(),
                    otp=key,
                    expiry=f"{settings.OTP_EXPIRY} seconds"
                )
            )
            msg = "otp has been sent to user's email"
            expiry = {"expiry": f"{settings.OTP_EXPIRY} seconds"}
        except ObjectDoesNotExist:
            msg = "invalid email"

        return Response({
            "success": True,
            "responseMessage": msg,
            "responseBody": expiry
        })


class VerifyResetPassword(APIView):
    """
    Verify the sent OTP and reset the associated user's password
    with the password signed on the OTP
    """
    serializer_class = VerifyOtpSerializer

    def post(self, request):

        serializer_class = VerifyOtpSerializer(data=request.POST)
        if serializer_class.is_valid():
            return Response({"success": True, "responseMessage": "password changed"})
        return Response({
            "success": False,
            "responseBody": serializer_class.error_messages
        }, status=status.HTTP_400_BAD_REQUEST)





class ChangeUserPasswordView(APIView):

    serializer_class = PasswordChangeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, requests):
        serializer = PasswordChangeSerializer(data=requests.data)
        if serializer.is_valid():
            # Check if the old password is correct
            if check_password(serializer.data['old_password'], requests.user.password):
                print(requests.user.password)
                new_pswd_hash = make_password(serializer.data['new_password'])
                requests.user.password = new_pswd_hash
                requests.user.save()
                return Response({
                    "success": True,
                    "responseMessage": "successful password change"
                })
            return Response({
                "success": False,
                "responseMessage": "incorrect password"
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            "success": False,
            "responseMessage": serializer.errors
        })


class ForgottenUsernameView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        # Send a mail to the user
        print("Confirmation email has been sent to user")
        send_email(
            subject="Request for Username",
            recipient_email=request.user.email,
            message=USERNAME_REQUEST_MESSAGE.format(
                username=request.user.username, full_name=request.user.get_full_name()
            )

        )
        return Response({
            "success": True,
            "responseMessage": "retrieval successful",
            "responseBody": "An email containing your username and password has been to sent to the registered email address"
        })
