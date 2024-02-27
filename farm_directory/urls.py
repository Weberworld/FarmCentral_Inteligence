from django.urls import path
from . import views

urlpatterns = [
    path("accounts/register", views.FarmersRegistrationView.as_view(), name="farm_directory.register"),
    path("search/<key>", views.KeywordSearchFarmDirectoryView.as_view(), name="farm_directory.search"),

    path("get/user/profile", views.UserProfileView.as_view(), name='profile')
]