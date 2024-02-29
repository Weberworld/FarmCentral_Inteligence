from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework.authtoken.models import Token

from .models import Account
from .serializers import UserLoginSerializer, PasswordChangeSerializer


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
                print(requests.user.password)
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
        send_mail(
            subject="Request for Username",
            message=f""
                    "We receive a request for your username. Below are your username and email\n\n"
                    
                    f"Your username: {request.user.username}\n"
                    f"Email: {request.user.email}\n\n"
                    f"We prioritize the safety of our farmers data.\n"
                    f"Please reset your password if you do not make this request.\n\n"
                    f"Thanks.\n"
                    f"Farm Central Intelligence!!",
            recipient_list=[request.user.email],
            from_email="support@farmci.com"
        )
        return Response({
            "success": True,
            "responseMessage": "retrieval successful",
            "responseBody": "An email containing your username and password has been to sent to the registered email address"
        })
