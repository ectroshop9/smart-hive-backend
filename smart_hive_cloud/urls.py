from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/devices/', include('devices.urls')),   # ← فوق
    path('api/readings/', include('readings.urls')),
    path('api/firmware/', include('firmware.urls')),
    path('api/store/', include('store.urls')),
    path('vault/', include('vault.urls')),
    path('', include('accounts.urls')),  # ← تحت
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
