from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_available=True)
        data = list(products.values('product_id', 'name', 'price', 'category', 'stock_quantity', 'image_url'))
        return Response(data)
