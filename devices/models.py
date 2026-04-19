from django.db import models
from users.models import Beekeeper

class Device(models.Model):
    DEVICE_TYPES = [
        ('MASTER', 'Master'),
        ('SLAVE', 'Slave'),
    ]

    device_id = models.CharField(max_length=10, primary_key=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(Beekeeper, on_delete=models.CASCADE, related_name='devices')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='slaves')
    firmware_version = models.CharField(max_length=20, default='1.0.0')
    last_seen = models.DateTimeField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'devices'
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return f"{self.device_id} - {self.name}"
