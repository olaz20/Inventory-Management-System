from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import logging
from apps.suppliers.v1.serializers import SupplierSerializer
from apps.suppliers.models import Supplier
from common.permission import IsSuperuser


logging = logging.getLogger(__name__)


class SupplierListCreateApiView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]

    def perform_create(self, serializer):
        try: 
           serializer.save()
           logging.info(f"Created supplier: {serializer.validated_data['name']}")
        except Exception as e:
            logging.error(f"Error creating supplier: {e}")
            raise 
    
class SupplierRetriveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]

    def perform_update(self, serializer):
        try:
            serializer.save()
            logging.info(f"Updated supplier: {serializer.validated_data['name']}")
        except Exception as e:
            logging.error(f"Error updating supplier: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            instance.delete()
            logging.info(f"Deleted supplier: {instance.name}")
        except  Exception as e:
            logging.error(f"Error deleting supplier: {e}")
            raise
