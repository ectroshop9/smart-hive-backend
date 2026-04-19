from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/readings/', include('readings.urls')),
    path('api/devices/', include('devices.urls')),
    path('api/firmware/', include('firmware.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# إضافة مسارات accounts
urlpatterns += [path('', include('accounts.urls'))]
