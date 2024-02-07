from django.contrib import admin
from .models import Account


# Account Admin page manager
class AccountManager(admin.ModelAdmin):
    exclude = ['user_permissions', "groups", "password", "superuser_status"]
    list_filter = ("is_director", "is_farmer")


admin.site.register(Account, AccountManager)
