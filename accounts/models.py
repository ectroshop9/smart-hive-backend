from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_serial_key():
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"SMART-{part1}-{part2}"

class SerialKey(models.Model):
    key = models.CharField(max_length=20, unique=True, default=generate_serial_key)
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    max_devices = models.IntegerField(default=11)

    class Meta:
        db_table = 'serial_keys'
        verbose_name = 'Serial Key'
        verbose_name_plural = 'Serial Keys'

    def __str__(self):
        return f"{self.key} ({'Used' if self.is_used else 'Available'})"
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_serial_key()
        super().save(*args, **kwargs)
