from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("account.urls")),
    path("farm_directory/", include("farm_directory.urls"))
]
