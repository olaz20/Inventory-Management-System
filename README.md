# 📦 Inventory Management System

A **Django REST Framework (DRF)** application for managing products, suppliers, and inventory levels.

🌐 **Live Demo**: [inventory-management-system-7t9o.onrender.com](https://inventory-management-system-7t9o.onrender.com)

This system supports:
- 🔄 CSV file uploads for bulk imports
- ⚙️ Asynchronous report generation with Celery & Redis
- 🔐 Secure superuser authentication

**Tech Stack**: Django, PostgreSQL, Celery, Redis  
**Hosting**: Render  
**Designed For**: Scalability, security, and efficient data processing

---

## 🚀 Features

### 🔐 1. Authentication

- **POST** `/v1/accounts/login/` (superuser only)
- Authenticates superusers & returns token.
- Uses `TokenAuthentication` and `IsSuperUser` permission class.

---

### 📦 2. Product Management

**Endpoints**:

- `GET /v1/product/products/` – List all products (with pagination, search, and ordering)
- `POST /v1/product/products/` – Create new product (superuser only)
- `GET /v1/product/products/<id>/` – Retrieve specific product
- `PUT /v1/product/products/<id>/` – Update product (superuser only)
- `DELETE /v1/product/products/<id>/` – Delete product (superuser only)

**Fields**:  
`name` (unique), `description`, `price`, `quantity`, `supplier` (FK)

---

### 🧾 3. Supplier Management

**Endpoints**:

- `GET /v1/supplier/`
- `POST /v1/supplier/` (superuser only)
- `GET /v1/supplier/<id>/`
- `PUT /v1/supplier/<id>/` (superuser only)
- `DELETE /v1/supplier/<id>/` (superuser only)

**Fields**:  
`name` (unique), `contact_info`

---

### 📊 4. Inventory Levels

**Endpoints**:

- `GET /v1/product/inventory/` – List inventory (pagination + filtering)
- `POST /v1/product/inventory/` – Add/update inventory (superuser only)

**Fields**:  
`product_id`, `product_name` (read-only), `quantity`, `updated_at`

📝 One-to-one validation between products and inventory. No duplicates or negative values allowed.

---

### 📥 5. CSV Product Upload

**Endpoint**: `POST /v1/product/upload-csv/` (superuser only)  
Import products in bulk using a CSV file.

**CSV Format**:

```csv
name,description,price,quantity,supplier_name
iPhone 15,Latest iPhone model with A17 chip,1099.99,100,Apple Inc.
MacBook Air,M2-powered lightweight laptop,1299.99,50,Apple Inc.
Galaxy Z Fold 6,Innovative foldable smartphone,1799.99,75,Samsung
AirPods Pro 2,Wireless earbuds with noise cancellation,249.99,200,Apple Inc.
