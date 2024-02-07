from farmci import settings
from django.db import models

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
)

STATE_CHOICES = (
    ("Abia", "Abia"),
    ("Adamawa", "Adamawa"),
    ("Akwa Ibom", "Akwa Ibom"),
    ("Anambra", "Anambra"),
    ("Bauchi", "Bauchi"),
    ("Bayelsa", "Bayelsa"),
    ("Benue", "Benue"),
    ("Borno", "Borno"),
    ("Cross River", "Cross River"),
    ("Delta", "Delta"),
    ("Ebonyi", "Ebonyi"),
    ("Edo", "Edo"),
    ("Ekiti", "Ekiti"),
    ("Enugu", "Enugu"),
    ("Gombe", "Gombe"),
    ("Imo", "Imo"),
    ("Jigawa", "Jigawa"),
    ("Kaduna", "Kaduna"),
    ("Kano", "Kano"),
    ("Katsina", "Katsina"),
    ("Kebbi", "Kebbi"),
    ("Kogi", "Kogi"),
    ("Kwara", "Kwara"),
    ("Lagos", "Lagos"),
    ("Nasarawa", "Nasarawa"),
    ("Niger", "Niger"),
    ("Ogun", "Ogun"),
    ("Ondo", "Ondo"),
    ("Osun", "Osun"),
    ("Oyo", "Oyo"),
    ("Plateau", "Plateau"),
    ("Rivers", "Rivers"),
    ("Sokoto", "Sokoto"),
    ("Taraba", "Taraba"),
    ("Yobe", "Yobe"),
    ("Zamfara", "Zamfara"),
)


class FarmDirectory(models.Model):
    """
    Table for farmers Directory profile
    """

    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    crop_type = models.CharField(max_length=20, null=True)
    bvn = models.SmallIntegerField(unique=True, null=True, blank=True)
    nin = models.SmallIntegerField(unique=True, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True)
    lga = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"Farm Profile for {self.account.username}"

