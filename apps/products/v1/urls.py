from django.urls import path
from .views import ProductListCreateApiView, ProductRetrieveUpdateDeleteApiView, InventoryLevelListCreateApiView, CSVUploadView

urlpatterns = [
    path('products/', ProductListCreateApiView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteApiView.as_view(), name='product-detail'),
    path('inventory/', InventoryLevelListCreateApiView.as_view(), name='inventory-list-create'),
    path('upload-csv/', CSVUploadView.as_view(), name='csv-upload'),
]

