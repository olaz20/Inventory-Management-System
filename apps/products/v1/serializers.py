from rest_framework import serializers
from ..models import Product
from apps.suppliers.models import Supplier

class ProductSerializer(serializers.ModelSerializer):
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), source='supplier', write_only=True)
    supplier = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'supplier_id', 'supplier', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at', 'supplier']

        def validate(self, attrs):
            if not attrs.get('name'):
                raise serializers.ValidationError("Product name is required.")
            if attrs.get('price') <= 0:
                raise serializers.ValidationError("Price must be greater than zero.")
            if attrs.get('quantity') < 0:
                raise serializers.ValidationError("Quantity cannot be negative.")
            return attrs
