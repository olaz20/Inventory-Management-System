from rest_framework import serializers
from ..models import Product, Inventorylevel
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

class InventoryLevelSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Inventorylevel
        fields = ["id", "product_id", "product" ,"quantity","updated_at"]
        read_only_field = ["id", "updated_at", "product"]
    def validate(self, attrs):
        product = attrs.get("product")
        quantity= attrs.get("quantity")
        if product and Inventorylevel.objects.filter(product=product).exists():
            if self.instance and self.instance.product != product:
                raise serializers.ValidationError({"product_id": "This product already has an inventory record"})
            elif not self.instance:
                raise serializers.ValidationError({"product_id":"This product already has an inventory record." })
            if quantity < 0:
                raise serializers.ValidationError({"quantity": "Quantity cannot be negative."})
        return attrs     
    
    def create(self, validated_data):
        product = validated_data["product"]
        product.quantity = validated_data["quantity"]
        product.save()
        return super().create(validated_data)

    def update(self, validated_data):
        product = validated_data.get("product", self.instance.product)
        product.quantity = validated_data.get("quantity", self.instance.quantity)
        product.save()
        return super().update(self.instance, validated_data)

class ProductCSVSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=0)
    supplier_name = serializers.CharField(max_length=200)

    def validate(self, attrs):
        supplier_name = attrs.get('supplier_name')
        if not Supplier.objects.filter(name=supplier_name).exists():
            raise serializers.ValidationError({"supplier_name": "Supplier does not exist."})
        
        if Product.objects.filter(name=attrs.get('name')).exists():
            raise serializers.ValidationError({"name": "Product with this name already exists."})
        return attrs
    def create(self, validated_data):
        supplier = Supplier.objects.get(name=validated_data['supplier_name'])
        product = Product.objects.create(
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            price=validated_data['price'],
            quantity=validated_data['quantity'],
            supplier=supplier
        )
        return product
    
        