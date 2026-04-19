from django.db import models
from devices.models import Device

class SensorReading(models.Model):
    STATE_CHOICES = [
        ('NORMAL', 'Normal'),
        ('SWARMING', 'Swarming'),
        ('SICK', 'Sick'),
        ('QUEENLESS', 'Queenless'),
        ('HONEY_FLOW', 'Honey Flow'),
        ('WINTERING', 'Wintering'),
        ('UNKNOWN', 'Unknown'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    temperature_1 = models.FloatField(blank=True, null=True)
    temperature_2 = models.FloatField(blank=True, null=True)
    temperature_3 = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    co2 = models.IntegerField(blank=True, null=True)
    sound = models.IntegerField(blank=True, null=True)
    light_level = models.IntegerField(blank=True, null=True)
    uv_index = models.IntegerField(blank=True, null=True)
    battery_level = models.IntegerField(blank=True, null=True)
    battery_health = models.IntegerField(blank=True, null=True)
    signal_rssi = models.IntegerField(blank=True, null=True)
    motion_detected = models.BooleanField(default=False)
    vibration_detected = models.BooleanField(default=False)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='UNKNOWN')

    class Meta:
        db_table = 'sensor_readings'
        verbose_name = 'Sensor Reading'
        verbose_name_plural = 'Sensor Readings'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.device.device_id} - {self.timestamp}"
