from django.utils import timezone
from djongo import models as models
TAG_CHOICES = ["shopify", "monetized", "consumable"]


class InventoryItem(models.Model):
    user_id = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    tags = models.JSONField(null=True, blank=True, default=[])
    category = models.CharField(max_length=100, default='')
    in_stock = models.FloatField()
    available_stock = models.FloatField()
    created = models.DateTimeField(default=timezone.now)
