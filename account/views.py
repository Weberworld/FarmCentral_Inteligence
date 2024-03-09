from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework.authtoken.models import Token

from account.serializers import UserLoginSerializer, PasswordChangeSerializer

from assets.emails.mail import send_email
from assets.emails.email_messages import PASSWORD_RESET_MESSAGE


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
            message=PASSWORD_RESET_MESSAGE.format(
                username=request.user.username, full_name=request.user.get_full_name()
            )

        )
        return Response({
            "success": True,
            "responseMessage": "retrieval successful",
            "responseBody": "An email containing your username and password has been to sent to the registered email address"
        })
