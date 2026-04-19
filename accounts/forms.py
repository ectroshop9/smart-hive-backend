from django import forms
from django.contrib.auth.models import User
from .models import SerialKey

class ActivationForm(forms.Form):
    serial_key = forms.CharField(max_length=20, label='كود التفعيل')
    name = forms.CharField(max_length=100, label='الاسم الكامل')
    email = forms.EmailField(label='البريد الإلكتروني')
    phone = forms.CharField(max_length=20, label='رقم الهاتف')
    password = forms.CharField(widget=forms.PasswordInput, label='كلمة المرور')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='تأكيد كلمة المرور')
    address = forms.CharField(widget=forms.Textarea, label='عنوان الشحن', required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('هذا البريد مسجل مسبقاً')
        return email

    def clean_serial_key(self):
        key = self.cleaned_data.get('serial_key')
        try:
            serial = SerialKey.objects.get(key=key)
            if serial.is_used:
                raise forms.ValidationError('هذا الكود مستخدم مسبقاً')
        except SerialKey.DoesNotExist:
            raise forms.ValidationError('كود التفعيل غير صحيح')
        return key
