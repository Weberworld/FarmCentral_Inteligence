from rest_framework import serializers

from account.models import Account
from account.serializers import UserAccountSerializer
from utils.utils import generate_random_string
from .models import FarmDirectory


class FarmerDirectoryRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class for farm directory registration
    """

    account = UserAccountSerializer()


    class Meta:
        model = FarmDirectory
        exclude = ['bvn', 'nin']

    def create(self, validated_data):


        user_data = validated_data.pop("account")
        user_data['username'] = f"FCI|{user_data['first_name'][0:3]}|{generate_random_string()}"


        user = Account.objects.create_user(**user_data)
        user.is_farmer = True
        user.save()
        farm_directory = FarmDirectory.objects.create(account=user, **validated_data)
        return farm_directory

    def to_representation(self, instance):
        """
        Override the default representation of django models Serializer
        """
        rep = super(FarmerDirectoryRegistrationSerializer, self).to_representation(instance)
        account_keys = rep['account'].keys()
        for key in account_keys:
            if rep["account"][key] == "first_name" or rep["account"][key] == "last_name":
                rep[key] = rep["account"][key].title()
            else:
                rep[key] = rep["account"][key]
        rep.pop("account")
        return rep


class FarmerProfileSerializer(serializers.ModelSerializer):
    account = UserAccountSerializer()


    class Meta:
        model = FarmDirectory
        exclude = ["bvn", "nin"]

    def to_representation(self, instance):
        rep = super(FarmerProfileSerializer, self).to_representation(instance)
        account_keys = rep['account'].keys()
        for key in account_keys:
            rep[key] = rep["account"][key]
        rep.pop("account")
        rep.pop("password")
        rep.pop("id")
        return rep


class EditFarmProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = FarmDirectory
        required = False
        exclude = ['account', 'nin', 'bvn']

        class Meta:
            model = FarmDirectory


    def is_valid(self, *, raise_exception=True):
        """
        Extends the default is_valid with checking if expected data are passed
        """
        super().is_valid()
        try:
            # print(self.fields)
            if [each for each in self.validated_data.keys() if each in self.fields]:
                # print(temp)
                return True
            else:
                self.error_messages = "empty edit params"
                return False
        except AttributeError:

            return False



class ResultSearchDirectorySerializer(serializers.ModelSerializer):
    """
        Serializer class for farm directory search result. It ensures that only set data are rendered
    """

    unused_account_info = ["password", "email"]
    account = UserAccountSerializer()

    class Meta:
        model = FarmDirectory
        fields = ["account", 'state', "crop_type"]

    def to_representation(self, instance):
        """
        Override the default representation of the ModelSerializer
        """
        rep = super(ResultSearchDirectorySerializer, self).to_representation(instance)
        account_keys = rep['account'].keys()
        for key in account_keys:
            if key not in self.unused_account_info:
                rep[key] = rep["account"][key]
        rep.pop("account")
        return rep




class NinAndBvnUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["bvn", "nin"]
        required = False