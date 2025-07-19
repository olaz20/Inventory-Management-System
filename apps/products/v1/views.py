from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging
from apps.products.v1.serializers import ProductSerializer, InventoryLevelSerializer, ProductCSVSerializer
from django.db import transaction
import pandas as pd
from django_filters.rest_framework import DjangoFilterBackend
from apps.products.models import Product, Inventorylevel
from common.permission import IsSuperuser
from common.response import api_response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

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

class CSVUploadView(APIView):
    permission_classes = [IsAuthenticated, IsSuperuser]
    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('file')
            if not file:
                logging.warning("CSV upload attempted without file")
                return api_response(message="No file provided", 
                        data={"file": "CSV file is required"},status_code=status.HTTP_400_BAD_REQUEST)
            
            if not file.name.endswith('.csv'):
                logging.warning("CSV upload attempted with non-CSV file")
                return api_response(message="Invalid file type", 
                        data={"file": "Only CSV files are allowed"}, status_code=status.HTTP_400_BAD_REQUEST)
            required_columns = ['name', 'description', 'price', 'quantity', 'supplier_id']
            try:
                df = pd.read_csv(file)
            except Exception as e:
                logging.error(f"Error reading CSV file: {e}")
                return api_response(message="Error reading CSV file", 
                        data={"file": "Invalid CSV format"}, status_code=status.HTTP_400_BAD_REQUEST)
            
            if not all(col in df.columns for col in required_columns):
                missing_cols = [col for col in required_columns if col not in df.columns]
                logging.warning(f"Missing columns in CSV: {missing_cols}")
                return api_response(
                    message="Invalid CSV format",
                    errors={"file": f"Missing columns: {', '.join(missing_cols)}"},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            results = {
                'total_records': len(df),
                'successful': 0,
                'failed': 0,
                'errors': []
            }
            with transaction.atomic():
                for index, row in df.iterrows():
                    serializer = ProductCSVSerializer(data=row.to_dict())
                    if serializer.is_valid():
                        serializer.save()
                        results['successful'] += 1
                        logging.info(f"Imported product: {row['name']} from CSV")
                    else:
                        results['failed'] += 1
                        results['errors'].append({
                            'row': index + 2,  # CSV row numbers start at 1, +1 for header
                            'errors': serializer.errors
                        })
                        logging.warning(f"Failed to import row {index + 2}: {serializer.errors}")
                message = "CSV processing completed"
            if results['failed'] > 0:
                message = "CSV processing completed with errors"
                status_code = status.HTTP_207_MULTI_STATUS
            else:
                status_code = status.HTTP_201_CREATED

            logging.info(f"CSV upload processed: {results['successful']} successful, {results['failed']} failed")
            return api_response(
                message=message,
                data=results,
                status_code=status_code
            )
        except Exception as e:
            logging.error(f"Unexpected error during CSV upload: {str(e)}")
            return api_response(
                message="Failed to process CSV",
                data={"detail": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )