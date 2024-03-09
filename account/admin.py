from django.contrib import admin
from .models import Account


# Account Admin page manager
class AccountManager(admin.ModelAdmin):
    exclude = ['user_permissions', "groups", "password", "superuser_status"]
    list_filter = ("is_director", "is_farmer", "date_joined")
    search_fields = ['date_joined', "email", "username", "first_name", "last_name"]


admin.site.register(Account, AccountManager)
admin.site.site_title = "FarmCI"
admin.AdminSite.site_header = "FarmCI"
