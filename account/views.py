from rest_framework import status
from rest_framework.views import Response, APIView
from rest_framework.authtoken.models import Token
from .serializers import UserLoginSerializer


class UserLoginView(APIView):
    """
    Logs in a user profile

    Returns: authentication token
    """
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, requests):
        serializer = UserLoginSerializer(data=requests.POST)
        if serializer.is_valid():
            user = serializer.authenticate()
            if user:
                # Return the authentication token if credentials is valid
                auth_token, created = Token.objects.get_or_create(user=user)
                return Response({"success": True, "message": "login success", "token": auth_token.key})
            else:
                return Response({'success': False, "message": serializer.error_messages}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error_messages": serializer.errors}, status=status.HTTP_404_NOT_FOUND)
