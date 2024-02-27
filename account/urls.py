from django.urls import path
from . import views

urlpatterns = [
    path('login', views.UserLoginView.as_view(), name="account.login"),
    path("change/password", views.ChangeUserPasswordView.as_view(), name="account.change_password"),
    path("forgot/username", views.ForgottenUsernameView.as_view(), name="account.forgot_username"),

]