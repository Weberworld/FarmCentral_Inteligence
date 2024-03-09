from django.db import models
from django.contrib.auth.models import AbstractUser
from farmci import settings


class Account(AbstractUser):

    phone = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    is_director = models.BooleanField(default=False, verbose_name="Director")
    is_farmer = models.BooleanField(default=False, verbose_name="Farmer")

    def __str__(self):
        self.get_full_name()
        return f"Account for {self.username}"



# class OTP(models.Model):
#
#     key = models.CharField(_("KEY"), primary_key=True, max_length=6, verbose_name="OTP Token")
#     created = models.BooleanField(default=False)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         verbose_name=_("User")
#     )
#
#     def create(self):



