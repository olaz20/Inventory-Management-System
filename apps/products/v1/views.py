from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging
from apps.products.v1.serializers import ProductSerializer, InventoryLevelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.products.models import Product, Inventorylevel
from common.permission import IsSuperuser
from common.response import api_response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


logging = logging.getLogger(__name__)

class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'supplier__id']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'quantity', 'created_at']
    ordering = ['name']
    pagination_class = PageNumberPagination
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
        

class InventoryLevelListCreateApiView(generics.ListCreateAPIView):
    queryset = Inventorylevel.objects.all()
    serializer_class = InventoryLevelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_filters = ['product__name']
    ordering_fields = ['product__name', 'quantity', 'updated_at']
    ordering = ['product__name']
    pagination_class = PageNumberPagination
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsSuperuser()]
        return [AllowAny()]
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logging.debug(f"Inventory levels retrieved by {request.user.username if request.user.is_authenticated else 'anonymous'}")
                return self.get_paginated_response(
                    api_response(
                        message="Inventory levels retrieved successfully",
                        data=serializer.data,
                        status_code=status.HTTP_200_OK
                    ).data
                )
            serializer = self.get_serializer(queryset, many=True)
            logging.debug(f"Inventory levels retrieved by {request.user.username if request.user.is_authenticated else 'anonymous'}")
            return api_response(
                message="Inventory levels retrieved successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            logging.error(f"Error retrieving inventory levels: {e}")
            return api_response(message="Error retrieving inventory levels", status_code=status.HTTP_400_BAD_REQUEST)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logging.info(f"Inventory level updated for product ID {serializer.validated_data['product'].id} by {request.user.username}")
            return api_response(
                message="Inventory level updated successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            logging.error(f"Error creating inventory level: {e}")
            return api_response(
                message="Failed to update inventory level",
                data={"detail": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

