from rest_framework import serializers
from kaizntree.models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['user_id', 'sku', 'name', 'tags', 'category', 'in_stock', 'available_stock']