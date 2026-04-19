from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ActivationForm
from .models import SerialKey
from users.models import Beekeeper
from devices.models import Device

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
