from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from account.models import Account
from account.serializers import UserLoginSerializer
from farm_directory.models import FarmDirectory
from farm_directory.serializers import FarmerDirectoryRegistrationSerializer, \
    ResultSearchDirectorySerializer, FarmerProfileSerializer
from utils.utils import parse_search_key


class FarmersRegistrationView(APIView):
    """
    Registers a new farmer into FarmCi Farm Directory

    method: POST
    Endpoint url: "base_url/accounts/register

    """
    serializer_class = FarmerDirectoryRegistrationSerializer

    @staticmethod
    def post(request):
        serializer = FarmerDirectoryRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Gets the user email from the serialized data
            user_email = serializer.data['email']
            # Get the user password from the serialized data
            try:
                password = serializer.initial_data['account.password']
            except KeyError:
                password = serializer.initial_data['account']["password"]
            # Get the user model from the db
            user_account = Account.objects.get(email=user_email)
            # Serialize the user login details
            login_serializer = UserLoginSerializer({"username": user_account.username, "password": password})
            login_serializer.data['login_url'] = reverse("account.login")
            return Response({"success": True, "responseMessage": "success", "responseBody": {
                "login": login_serializer.data},
                "message": f"{user_account.username} has been registered",
                "info": "Proceed to login to get authentication token",
            })

        else:
            return Response({
                "success": False, "responseMessage": "used credentials", "responseBody": {"errors": serializer.errors}
            }, status.HTTP_400_BAD_REQUEST)


# Profile Details View
class UserProfileView(APIView):
    """
    Gets the user farm details
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        print(request)
        serializer = FarmerProfileSerializer(request.user.farmdirectory)
        # Remove the password field from the response data

        return Response({
            "success": True, "responseMessage": "profile retrieved successful",
            "responseBody": {
                "user": serializer.data
            }
        })



# Filter Endpoint
class KeywordSearchFarmDirectoryView(APIView):
    pagination_class = []

    @staticmethod
    def get(_, key):
        search_keyword = parse_search_key(key)
        farm_directory = FarmDirectory.objects.all()
        matches = []
        for entry in farm_directory:
            try:
                if search_keyword == "phone":
                    if entry.account.phone.startswith(key) or key in entry.account.phone:
                        matches.append(entry)

                elif search_keyword == "state":
                    if entry.state.lower().startswith(key) or key in entry.state.lower():
                        matches.append(entry)

                elif search_keyword == "crop_type":
                    if entry.crop_type.lower().startswith(key) or key in entry.crop_type.lower():
                        matches.append(entry)

                continue
            except AttributeError:
                continue
        results = ResultSearchDirectorySerializer(matches, many=True)

        if matches:
            return Response({
                "success": True, "responseMessage": "success",
                "responseBody": {
                    "keyword": search_keyword,
                    "no_of_matches": len(matches),
                    "results": results.data
                }
            })
        else:
            return Response({
                "success": True, "responseMessage":  "no match",
                "responseBody": "no match"
            }, status=status.HTTP_404_NOT_FOUND)
