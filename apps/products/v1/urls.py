from django.urls import path
from .views import ProductListCreateApiView, ProductRetrieveUpdateDeleteApiView

urlpatterns = [
    path('products/', ProductListCreateApiView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteApiView.as_view(), name='product-detail'),
]