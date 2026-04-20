from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Product, Order, OrderItem
from users.models import Beekeeper

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_available=True)
        data = list(products.values(
            'product_id', 'name', 'description', 'category', 
            'price', 'stock_quantity', 'image_url'
        ))
        return Response(data)

class ProductDetailAPIView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            data = {
                'product_id': product.product_id,
                'name': product.name,
                'description': product.description,
                'category': product.category,
                'price': str(product.price),
                'stock_quantity': product.stock_quantity,
                'image_url': product.image_url,
                'is_available': product.is_available
            }
            return Response(data)
        except Product.DoesNotExist:
            return Response({'error': 'المنتج غير موجود'}, status=404)

class CreateOrderAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', 'BEEK-GUEST')
        full_name = request.data.get('full_name', 'زائر')
        phone = request.data.get('phone', '0000000000')
        items = request.data.get('items', [])
        shipping_address = request.data.get('shipping_address', '')
        
        # إنشاء أو جلب المستخدم (زائر أو مسجل)
        beekeeper, created = Beekeeper.objects.get_or_create(
            user_id=user_id,
            defaults={
                'name': full_name,
                'phone': phone,
                'email': f"{user_id}@guest.com"
            }
        )
        
        # إذا كان المستخدم موجوداً مسبقاً وزائر، نحدث بياناته
        if not created and user_id == 'BEEK-GUEST':
            beekeeper.name = full_name
            beekeeper.phone = phone
            beekeeper.save()
        
        # إنشاء الطلب
        order_id = f"ORD{timezone.now().strftime('%y%m%d%H%M%S')}"
        total = 0
        
        order = Order.objects.create(
            order_id=order_id,
            user=beekeeper,
            total_amount=0,
            shipping_address=shipping_address,
            status='PENDING'
        )
        
        # إضافة المنتجات
        for item in items:
            try:
                product = Product.objects.get(product_id=item['product_id'])
                quantity = item['quantity']
                unit_price = product.price
                total_price = unit_price * quantity
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                total += total_price
                
                # تحديث المخزون
                product.stock_quantity -= quantity
                product.save()
            except Product.DoesNotExist:
                continue
        
        order.total_amount = total
        order.save()
        
        return Response({
            'success': True,
            'order_id': order.order_id,
            'total': str(total)
        }, status=201)

class OrderHistoryAPIView(APIView):
    def get(self, request, user_id):
        try:
            beekeeper = Beekeeper.objects.get(user_id=user_id)
            orders = Order.objects.filter(user=beekeeper).order_by('-order_date')
            data = []
            for order in orders:
                items = list(order.items.values(
                    'product__name', 'quantity', 'unit_price', 'total_price'
                ))
                data.append({
                    'order_id': order.order_id,
                    'order_date': order.order_date,
                    'total_amount': str(order.total_amount),
                    'status': order.status,
                    'items': items
                })
            return Response(data)
        except Beekeeper.DoesNotExist:
            return Response({'error': 'المستخدم غير موجود'}, status=404)
