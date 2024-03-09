from django.urls import path, include
from . import views

user_profile_patters = [
    path("update", views.UpdateVerificationView.as_view(), name="farm_directory.update_bvn_or_nin")
]

urlpatterns = [
    path("accounts/register", views.FarmersRegistrationView.as_view(), name="farm_directory.register"),
    path("search/<key>", views.KeywordSearchFarmDirectoryView.as_view(), name="farm_directory.search"),
    path("users/farm/profile/", include(user_profile_patters)),


    path("users/farm/get/profile", views.UserProfileView.as_view(), name='farm_directory.profile'),
]