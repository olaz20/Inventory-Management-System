from rest_framework import serializers
from apps.suppliers.models import  Supplier
from apps.products.models import Product, Inventorylevel
import phonenumbers

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "contact_email", "phone_number", "address"]

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number format.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")
        return attrs
        
        
        