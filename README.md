Inventory Management System
A Django REST Framework (DRF) application for managing products, suppliers, and inventory levels, hosted at https://inventory-management-system-7t9o.onrender.com. The system supports CSV file uploads for bulk product imports, asynchronous report generation using Celery and Redis, and secure superuser authentication. It is deployed on Render with PostgreSQL for data storage and Redis for task queuing, designed for scalability, security, and efficient data processing.
Features
1. Authentication

Endpoint: POST /v1/accounts/login/ (superuser only)
Authenticates superusers and generates a token for accessing restricted endpoints.
Uses TokenAuthentication with IsSuperUser permission for secure access.



2. Product Management

Endpoints:
GET /v1/product/products/: List all products with pagination, filtering (e.g., search, ordering), accessible to all users.
POST /v1/product/products/: Create a new product (superuser only).
GET /v1/product/products/<id>/: Retrieve a specific product (open to all users).
PUT /v1/product/products/<id>/: Update a product (superuser only).
DELETE /v1/product/products/<id>/: Delete a product (superuser only).


Fields: name (unique, max 255 chars), description (optional), price (decimal, positive), quantity (non-negative integer), supplier (linked to Supplier model).

3. Supplier Management

Endpoints:
GET /v1/supplier/: List all suppliers with pagination and filtering (open to all users).
POST /v1/supplier/: Create a new supplier (superuser only).
GET /v1/supplier/<id>/: Retrieve a specific supplier (open to all users).
PUT /v1/supplier/<id>/: Update a supplier (superuser only).
DELETE /v1/supplier/<id>/: Delete a supplier (superuser only).


Fields: name (unique), contact_info.

4. Inventory Levels

Endpoint: GET/POST /v1/product/inventory/
GET: List inventory levels for all products with pagination and filtering (open to all users).
POST: Create or update inventory levels for a product (superuser only).


Fields: product_id, product_name (read-only), quantity (non-negative), updated_at (timestamp).
Notes: Ensures one-to-one relationship between products and inventory records, with validation for duplicates and negative quantities.

5. CSV File Upload

Endpoint: POST /v1/product/upload-csv/ (superuser only)
Purpose: Import products from a CSV file.
CSV Format:name,description,price,quantity,supplier_name
iPhone 15,Latest iPhone model with A17 chip,1099.99,100,Apple Inc.
MacBook Air,M2-powered lightweight laptop,1299.99,50,Apple Inc.
Galaxy Z Fold 6,Innovative foldable smartphone,1799.99,75,Samsung
AirPods Pro 2,Wireless earbuds with noise cancellation,249.99,200,Apple Inc.


Validation:
Required columns: name, description, price, quantity, supplier_name.
Unique product names.
Positive prices (max 10 digits, 2 decimal places).
Non-negative quantities.
Existing supplier names.


Response: JSON with total records, successful/failed counts, and row-specific errors.

6. Report Generation

Endpoints:
POST /v1/common/reports/generate/: Start asynchronous report generation (superuser only).
GET /v1/common/reports/status/<task_id>/: Check report generation status (superuser only).
GET /v1/common/reports/download/<filename>/: Download generated report CSV (superuser only).


Reports:
Inventory Levels: Product ID, name, quantity, price, stock value, supplier, low stock alerts (quantity < 10).
Supplier Performance: Number of products and total stock value per supplier.


Technology: Celery for asynchronous processing, Redis as the message broker.
Output: Two CSV files (inventory_report_<timestamp>.csv, supplier_report_<timestamp>.csv) stored in the reports directory.

7. API Documentation

Endpoint: GET /
Access the Swagger UI for interactive API documentation at https://inventory-management-system-7t9o.onrender.com/.



8. Admin Interface

Endpoint: /secure-admin/ (superuser only)
Django admin panel for managing models directly.



9. Logging

All operations (e.g., product imports, report generation) are logged to inventory.log for auditing.

Postman Collection
Test the API using the Postman collection:

Invitation Link: Join the Postman team
Usage: Import the collection to test endpoints like login, CSV upload, and report generation.

Prerequisites

Python 3.8+
PostgreSQL
Redis (for Celery)
Render account
Git
Postman (for API testing)

Setup Instructions (Local)
1. Clone the Repository
git clone https://github.com/olaz20/Inventory-Management-System.git


2. Install Dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

requirements.txt:
django>=5.0
djangorestframework
django-filter
python-decouple
gunicorn
psycopg2-binary
celery
redis
pandas

3. Configure Environment Variables
Create a .env file in the project root:

ATABASE_HOST
DATABASE_PORT
DATABASE_USER
DATABASE_NAME
DATABASE_PASSWORD

SUPERUSER_USERNAME
DJANGO_SUPERUSER_EMAIL
DJANGO_SUPERUSER_PASSWORD

SECRET_KEY
DATABASE_URL

CELERY_BROKER_URL





4. Set Up PostgreSQL

Create a PostgreSQL database and update .env with credentials.
Apply migrations:python manage.py makemigrations
python manage.py migrate



5. Set Up Redis and Celery

Run Redis locally:docker run -d -p 6379:6379 redis


Start Celery worker:celery -A inventory_project worker --loglevel=info



6. Create a Superuser
python manage.py user_auto

7. Run the Server
python manage.py runserver


Access Swagger UI at http://127.0.0.1:8000/.
Access admin panel at http://127.0.0.1:8000/secure-admin/.

Create PostgreSQL Database

Test with Postman

Join the Postman team: Invitation Link.

https://app.getpostman.com/join-team?invite_code=ff5566144d43f2915ad2b14763d809d3d0ed79f5fd874ffab58acbe9c8810952&target_code=de7e888e61bf83ea9e5786d3b1365ad8



License
MIT License

Built with Django