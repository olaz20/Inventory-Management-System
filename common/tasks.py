from celery import shared_task
from apps.products.models import Product 
from apps.suppliers.models import Supplier
import pandas as pd
import os
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def generate_inventory_report(self):
    try:
        task_id = self.request.id
        LOW_STOCK_THRESHOLD = 50
        products = Product.objects.select_related('supplier').prefetch_related('inventory').all()

        inventory_data = []
        for product in products:
            inventory = getattr(product, 'inventory', None)
            quantity = inventory.quantity if inventory else product.quantity
            is_low_stock = quantity < LOW_STOCK_THRESHOLD
            inventory_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': quantity,
                'price': float(product.price),
                'stock_value': float(quantity * product.price),
                'supplier_name': product.supplier.name,
                'low_stock_alert': 'Yes' if is_low_stock else 'No',
            })
        # suppllier performance report
        suppliers = Supplier.objects.prefetch_related("products").all()
        supplier_data = []
        for supplier in suppliers:
            products = supplier.products.all()
            total_products = products.count()
            total_stock_value = sum(product.price * (product.inventory.quantity if product.inventory else product.quantity) for product in products)

            supplier_data.append({
                'supplier_name': supplier.name,
                'total_products': total_products,
                'total_stock_value': float(total_stock_value),
            })
            inventory_df  = pd.DataFrame(inventory_data)
            supplier_df = pd.DataFrame(supplier_data)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_dir = os.path.join(settings.BASE_DIR, 'reports')
            os.makedirs(report_dir, exist_ok=True)
            
            inventory_file = os.path.join(report_dir, f'inventory_report_{timestamp}.csv')
            supplier_file = os.path.join(report_dir, f'supplier_report_{timestamp}.csv')

            inventory_df.to_csv(inventory_file, index=False)
            supplier_df.to_csv(supplier_file, index=False)

            logger.info(f"Inventory report generated: {inventory_file}, Supplier report: {supplier_file}")
            return {
                'task_id': task_id,
                'status': 'completed',
                'inventory_file': inventory_file,
                'supplier_file': supplier_file,
                'message': 'Report generated successfully'
            }
    except Exception as e:
        logger.error(f"Error generating inventory report: {str(e)}")
        return {
            'task_id': task_id,
            'status': 'failed',
            'message': f'Failed to generate report: {str(e)}'
        }