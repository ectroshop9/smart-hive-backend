from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # صفحات HTML
    path('activate/', views.activate_view, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # API Endpoints
    path('api/activate/', views.ActivateAPIView.as_view(), name='api_activate'),
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
]
