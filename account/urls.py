from django.urls import path
from . import views

urlpatterns = [
    path('login', views.UserLoginView.as_view(), name="account.login"),
    path("reset/password", views.ResetUserPassword.as_view(), name="account.reset_password"),
    path("reset/password/verify", views.VerifyResetPassword.as_view(), name="account.validate_password_reset"),
    path("forgot/username", views.ForgottenUsernameView.as_view(), name="account.forgot_username"),

]