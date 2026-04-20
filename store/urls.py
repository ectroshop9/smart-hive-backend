from django.urls import path
from . import views

urlpatterns = [
    path('api/products/', views.ProductListAPIView.as_view(), name='api_products'),
    path('api/products/<str:product_id>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('api/orders/create/', views.CreateOrderAPIView.as_view(), name='api_create_order'),
    path('api/orders/<str:user_id>/', views.OrderHistoryAPIView.as_view(), name='api_order_history'),
]
