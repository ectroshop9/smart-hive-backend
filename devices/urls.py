from django.urls import path
from .views import RegisterDeviceAPIView, CheckinAPIView, DeviceListView

urlpatterns = [
    path('register/', RegisterDeviceAPIView.as_view(), name='register'),
    path('checkin/', CheckinAPIView.as_view(), name='checkin'),
    path('list/', DeviceListView.as_view(), name='device_list'),
]
