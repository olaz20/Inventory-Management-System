from django.db import models
from apps.suppliers.models import Supplier
from common.models import Audit



class Product(Audit):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey(
        "suppliers.Supplier", on_delete=models.CASCADE, related_name="products"
    )
    def __str__(self):
        return self.name

class Inventorylevel(Audit):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Inventory level for {self.product.name}: {self.quantity}"