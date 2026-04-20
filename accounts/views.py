from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import ActivationForm
from .models import SerialKey
from users.models import Beekeeper
from devices.models import Device
# ==================== إنشاء المسؤول تلقائياً ====================
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Admin user created: admin / admin123")

# ==================== Django Views (للصفحات) ====================

def activate_view(request):
    if request.method == 'POST':
        form = ActivationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['name']
            )
            
            beekeeper = Beekeeper.objects.create(
                user_id=f"BEEK-{user.id:04d}",
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data.get('address', '')
            )
            
            serial = SerialKey.objects.get(key=form.cleaned_data['serial_key'])
            serial.is_used = True
            serial.used_by = user
            serial.used_at = timezone.now()
            serial.save()
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = ActivationForm()
    
    return render(request, 'accounts/activate.html', {'form': form})


@login_required
def dashboard_view(request):
    try:
        beekeeper = Beekeeper.objects.get(email=request.user.email)
        devices = Device.objects.filter(user=beekeeper)
        
        context = {
            'beekeeper': beekeeper,
            'devices': devices,
        }
    except Beekeeper.DoesNotExist:
        context = {'error': 'الحساب غير مرتبط بنحال'}
    
    return render(request, 'accounts/dashboard.html', context)


# ==================== API Views (لـ React) ====================

@method_decorator(csrf_exempt, name='dispatch')
class ActivateAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            serial_key = data.get('serial_key')
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
            address = data.get('address', '')
            
            # التحقق من الكود
            try:
                serial = SerialKey.objects.get(key=serial_key, is_used=False)
            except SerialKey.DoesNotExist:
                return Response({'error': 'كود التفعيل غير صحيح'}, status=status.HTTP_400_BAD_REQUEST)
            
            # التحقق من عدم وجود مستخدم بنفس البريد
            if User.objects.filter(email=email).exists():
                return Response({'error': 'البريد الإلكتروني مستخدم مسبقاً'}, status=status.HTTP_400_BAD_REQUEST)
            
            # إنشاء المستخدم
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            
            # إنشاء النحال
            beekeeper = Beekeeper.objects.create(
                user_id=f"BEEK-{user.id:04d}",
                name=name,
                phone=phone,
                email=email,
                address=address
            )
            
            # تحديث الكود
            serial.is_used = True
            serial.used_by = user
            serial.used_at = timezone.now()
            serial.save()
            
            return Response({
                'success': True,
                'message': 'تم التفعيل بنجاح',
                'user_id': beekeeper.user_id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'البريد الإلكتروني غير موجود'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(username=user.username, password=password)
        if user is not None:
            return Response({
                'success': True,
                'token': 'dummy-token',
                'name': user.first_name,
                'email': user.email
            })
        else:
            return Response({'error': 'كلمة المرور غير صحيحة'}, status=status.HTTP_401_UNAUTHORIZED)
