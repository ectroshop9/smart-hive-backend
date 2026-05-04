from django.db import models

class Block(models.Model):
    mac = models.CharField(max_length=17)
    previous_hash = models.CharField(max_length=64)
    block_hash = models.CharField(max_length=64, unique=True)
    data_json = models.TextField()
    signature_b64 = models.TextField(blank=True, null=True)
    nonce = models.BigIntegerField(null=True)
    timestamp = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
