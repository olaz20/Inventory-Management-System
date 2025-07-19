from django.urls import path


from .views import SupplierListCreateApiView, SupplierRetriveUpdateDeleteApiView


urlpatterns = [
path('suppliers/', SupplierListCreateApiView.as_view(), name='supplier-list-create'),
path('suppliers/<int:pk>/',SupplierRetriveUpdateDeleteApiView.as_view(), name='supplier-detail'),
]