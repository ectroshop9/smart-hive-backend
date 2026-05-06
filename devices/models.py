from django.db import models
from users.models import Beekeeper

class Device(models.Model):
    DEVICE_TYPES = [
        ('MASTER', 'ماستر'),
        ('SLAVE', 'تابع'),
    ]

    name = models.CharField(max_length=100, verbose_name="اسم الجهاز")
    mac_address = models.CharField(max_length=17, unique=True, null=True, blank=True, verbose_name="MAC Address")
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, default='MASTER', verbose_name="نوع الجهاز")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    
    user = models.ForeignKey(Beekeeper, on_delete=models.CASCADE, related_name='devices', verbose_name="النحّال")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='slaves', verbose_name="الجهاز الأب")
    
    firmware_version = models.CharField(max_length=20, default='1.0.0', verbose_name="إصدار البرنامج")
    last_seen = models.DateTimeField(blank=True, null=True, verbose_name="آخر ظهور")
    is_online = models.BooleanField(default=False, verbose_name="متصل الآن")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    class Meta:
        db_table = 'devices'
        verbose_name = 'جهاز'
        verbose_name_plural = 'الأجهزة'
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.name} ({self.mac_address})"
class AuthorizedMAC(models.Model):
    mac_address = models.CharField(max_length=17, unique=True, verbose_name="MAC Address")
    is_registered = models.BooleanField(default=False, verbose_name="مسجل من نحّال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        db_table = 'authorized_macs'
        verbose_name = 'جهاز مرخص'
        verbose_name_plural = 'الأجهزة المرخصة'

    def __str__(self):
        return f"{self.mac_address} - {'مسجل' if self.is_registered else 'متاح'}"