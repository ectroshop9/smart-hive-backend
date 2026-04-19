from django.urls import path
from .views import CheckFirmwareAPIView, OTAStatusAPIView, FirmwareListView

urlpatterns = [
    path('check/', CheckFirmwareAPIView.as_view(), name='check_firmware'),
    path('status/', OTAStatusAPIView.as_view(), name='ota_status'),
    path('list/', FirmwareListView.as_view(), name='firmware_list'),
]
