from django.contrib import admin
from django.urls import path, include

from farmci import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("account.urls")),
    path("db/", include("farm_directory.urls"))
]

from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
