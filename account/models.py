from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):

    phone = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    is_director = models.BooleanField(default=False, verbose_name="Director")
    is_farmer = models.BooleanField(default=False, verbose_name="Farmer")

    def __str__(self):
        self.get_full_name()
        return f"Account for {self.username}"




