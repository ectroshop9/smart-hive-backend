from django.db import models

class Firmware(models.Model):
    DEVICE_TYPES = [
        ('MASTER', 'Master'),
        ('SLAVE', 'Slave'),
    ]

    firmware_id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    file_path = models.CharField(max_length=255)
    file_size = models.IntegerField(default=0)
    checksum = models.CharField(max_length=64)
    changelog = models.TextField(blank=True)
    is_stable = models.BooleanField(default=True)
    min_version = models.CharField(max_length=20, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'firmware'
        verbose_name = 'Firmware'
        verbose_name_plural = 'Firmwares'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.version} ({self.device_type})"


class OTASession(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('DOWNLOADING', 'Downloading'),
        ('VERIFYING', 'Verifying'),
        ('APPLYING', 'Applying'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    progress = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'ota_sessions'
        verbose_name = 'OTA Session'
        verbose_name_plural = 'OTA Sessions'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.device.device_id} - {self.firmware.version} ({self.status})"
