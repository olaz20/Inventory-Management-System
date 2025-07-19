from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging
from apps.products.v1.serializers import ProductSerializer
from apps.products.models import Product
from common.permission import IsSuperuser
from common.response import api_response

logging = logging.getLogger(__name__)

class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsSuperuser()]
        return [AllowAny()]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logging.info(f"Created product: {serializer.validated_data['name']}")
            return api_response(message="Product created successfully", data=serializer.data, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(f"Error creating product: {e}")
            return api_response(message="Error creating product", status_code=status.HTTP_400_BAD_REQUEST)
        
class ProductRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsSuperuser()]
        return [AllowAny()]
    
    def retrieve(self, request, *args, **kwargs):
        try:
           instance = self.get_object()
           serializer = self.get_serializer(instance)
           logger.debug(f"Product retrieved: ID {instance.id} by {request.user.username}")
           return api_response(message="Product retrived successfully", data=serializer.data, status_code=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Error retrieving product: {e}")
            return api_response(message="Error retrieving product", status_code=status.HTTP_404_NOT_FOUND)
    def perform_update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info(f"Product updated: ID {instance.id} by {request.user.username}")
            return api_response(message="Product updated successfully", data=serializer.data, status_code=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Error updating product: {e}")
            return api_response(message="Error updating product", status_code=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            logger.info(f"Product deleted: ID {instance.id} by {request.user.username}")
            self.perform_destroy(instance)
            return api_response(message="Product deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(f"Error deleting product: {e}")
            return api_response(message="Error deleting product", status_code=status.HTTP_400_BAD_REQUEST)
        