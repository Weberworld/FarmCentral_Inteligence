import random
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

from farmci import settings


class Account(AbstractUser):

    profile_img = models.FileField(null=True, blank=True, upload_to="images")
    phone = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    is_director = models.BooleanField(default=False, verbose_name="Director")
    is_farmer = models.BooleanField(default=False, verbose_name="Farmer")

    def __str__(self):
        self.get_full_name()
        return f"Account for {self.username}"



class OTP(models.Model):

    hash_key = models.CharField(primary_key=True, max_length=6)
    created = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User", null=True, blank=True
    )
    time_generated = models.DateTimeField(auto_now_add=True)
    signed_data = models.CharField(max_length=50, null=True, blank=True)

    def create(self, data):

        key = self.gen_key(data)
        self.time_generated = timezone.make_aware(datetime.now())
        return key

    def gen_key(self, data):
        """ Generate random values and sign a password on the OTP"""
        key = [random.randint(0, 9) for _ in range(settings.OTP_LENGTH)]
        self.hash_key = "".join(str(i) for i in key)
        self.signed_data = make_password(data)

        return self.hash_key

    def is_valid(self, key):
        """
        Returns True if the otp is valid and not expired.
        It reset the associated user's password
        """
        if (key == self.hash_key) and ((timezone.now() - self.time_generated).seconds <= settings.OTP_EXPIRY):
            self.user.password = self.signed_data
            self.user.save()
            self.delete()
            return True
        return False
