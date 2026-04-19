from django.urls import path
from .views import ReadingAPIView

urlpatterns = [
    path('', ReadingAPIView.as_view(), name='readings'),
]
