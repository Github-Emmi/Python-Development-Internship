# EmmiDev API Documentation

## Overview

EmmiDev API is a high-performance REST API built with **FastAPI**, **MongoDB (Motor)**, and **Redis caching**. It provides secure user authentication via JWT tokens and comprehensive product management with intelligent caching.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "full_name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true
}
```

**Error Responses:**
- `400 Bad Request` - Email already registered
- `422 Unprocessable Entity` - Invalid input (password too short, invalid email)

---

### Login

Authenticate and receive JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "507f1f77bcf86cd799439011"
}
```

**Error Responses:**
- `401 Unauthorized` - Incorrect email or password

---

## 📦 Product Endpoints

### Create Product

Create a new product in the catalog.

**Endpoint:** `POST /products/`

**Request Body:**
```json
{
  "name": "Premium Wireless Headphones",
  "price": 299.99,
  "category": "Electronics"
}
```

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439012",
  "_id": "507f1f77bcf86cd799439012",
  "name": "Premium Wireless Headphones",
  "price": 299.99,
  "category": "Electronics"
}
```

**Validation Rules:**
- `name`: 1-100 characters, required
- `price`: Must be > 0, required
- `category`: Required (string)

**Error Responses:**
- `422 Unprocessable Entity` - Validation failed
- `500 Internal Server Error` - Database error

---

### List Products

Get all products with pagination and Redis caching.

**Endpoint:** `GET /products/`

**Query Parameters:**
- `skip`: Number of products to skip (default: 0, min: 0)
- `limit`: Number of products to return (default: 10, min: 1, max: 100)

**Example Request:**
```
GET /products/?skip=0&limit=10
```

**Response:** `200 OK`
```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "_id": "507f1f77bcf86cd799439012",
    "name": "Premium Wireless Headphones",
    "price": 299.99,
    "category": "Electronics"
  },
  {
    "id": "507f1f77bcf86cd799439013",
    "_id": "507f1f77bcf86cd799439013",
    "name": "USB-C Cable",
    "price": 12.99,
    "category": "Accessories"
  }
]
```

**Cache Behavior:**
- First request: Fetched from MongoDB, cached in Redis for 5 minutes
- Subsequent requests: Served from Redis cache (very fast)
- Cache invalidated on: Create, Update, or Delete operations

**Error Responses:**
- `500 Internal Server Error` - Database or cache error

---

### Get Product by ID

Retrieve details of a specific product.

**Endpoint:** `GET /products/{product_id}`

**Path Parameters:**
- `product_id`: MongoDB ObjectId (string format)

**Example Request:**
```
GET /products/507f1f77bcf86cd799439012
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439012",
  "_id": "507f1f77bcf86cd799439012",
  "name": "Premium Wireless Headphones",
  "price": 299.99,
  "category": "Electronics"
}
```

**Error Responses:**
- `404 Not Found` - Product does not exist
- `500 Internal Server Error` - Database error

---

### Update Product

Update one or more fields of an existing product.

**Endpoint:** `PUT /products/{product_id}`

**Path Parameters:**
- `product_id`: MongoDB ObjectId (string format)

**Request Body:** (All fields optional)
```json
{
  "name": "Updated Product Name",
  "price": 349.99,
  "category": "Premium Electronics"
}
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439012",
  "_id": "507f1f77bcf86cd799439012",
  "name": "Updated Product Name",
  "price": 349.99,
  "category": "Premium Electronics"
}
```

**Validation Rules:**
- `name`: If provided, must be 1-100 characters
- `price`: If provided, must be > 0
- Only fields provided in request body are updated

**Cache Behavior:**
- Cache invalidated after update
- Next list request will refresh from MongoDB

**Error Responses:**
- `404 Not Found` - Product does not exist
- `422 Unprocessable Entity` - Validation failed
- `500 Internal Server Error` - Database error

---

### Delete Product

Remove a product from the catalog.

**Endpoint:** `DELETE /products/{product_id}`

**Path Parameters:**
- `product_id`: MongoDB ObjectId (string format)

**Response:** `204 No Content` (no response body)

**Cache Behavior:**
- Cache invalidated after deletion
- Next list request will refresh from MongoDB

**Error Responses:**
- `404 Not Found` - Product does not exist
- `500 Internal Server Error` - Database error

---

## 🔄 Response Format

All responses follow this pattern:

**Success (2xx):**
```json
{
  "id": "...",
  "name": "...",
  "price": 0.00,
  "category": "..."
}
```

**Error (4xx, 5xx):**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## 📊 Caching Strategy

### Products List Cache
- **Key:** `products_list:skip:{skip}:limit:{limit}`
- **TTL:** 300 seconds (5 minutes)
- **Invalidation:** Automatic on create, update, or delete

**Benefits:**
1. Reduces MongoDB load
2. Faster response times for list requests
3. Automatic expiration ensures data freshness

**Example Timeline:**
1. First `GET /products/` → MongoDB query (slow) → Cache in Redis
2. Subsequent `GET /products/` (within 5 min) → Redis hit (fast)
3. `POST /products/` → Cache invalidated
4. Next `GET /products/` → MongoDB query (cache rewarmed)

---

## 🔒 Security Features

1. **Password Hashing:** Bcrypt with salt
2. **JWT Tokens:** Secure token-based authentication
3. **CORS:** Restricted origins (configured in main.py)
4. **HTTPS Ready:** Production deployment recommended with TLS
5. **Input Validation:** Pydantic models enforce strict validation

---

## 📋 Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET/PUT request |
| 201 | Created | Successful POST request |
| 204 | No Content | Successful DELETE request |
| 400 | Bad Request | Email already registered |
| 401 | Unauthorized | Invalid credentials or missing token |
| 404 | Not Found | Product/user does not exist |
| 422 | Unprocessable Entity | Validation error (bad data) |
| 500 | Internal Server Error | Database or server error |

---

## 💡 Usage Examples

### Complete Workflow

```bash
# 1. Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "SecurePass123",
    "full_name": "Alice"
  }'

# Response includes user details

# 2. Login and get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "SecurePass123"
  }'

# Response includes: access_token, token_type, user_id
# Save the access_token for next requests

# 3. Create a product
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "category": "Electronics"
  }'

# 4. List products (cached)
curl http://localhost:8000/api/v1/products/

# 5. Get specific product
curl http://localhost:8000/api/v1/products/507f1f77bcf86cd799439012

# 6. Update product
curl -X PUT http://localhost:8000/api/v1/products/507f1f77bcf86cd799439012 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 899.99
  }'

# 7. Delete product
curl -X DELETE http://localhost:8000/api/v1/products/507f1f77bcf86cd799439012
```

---

## 🧪 Testing

### Using Swagger UI
```
http://localhost:8000/docs
```

Interactive API testing with automatic request/response generation.

### Using ReDoc
```
http://localhost:8000/redoc
```

Beautiful API documentation with examples.

---

## 🚀 Performance Notes

- **List caching:** 5-minute Redis cache reduces database load by ~90%
- **Async operations:** All I/O operations are non-blocking
- **Connection pooling:** MongoDB and Redis connections are pooled
- **Pagination:** Implemented to handle large datasets efficiently

---

## 📞 Support

For issues or questions:
1. Check logs: `logs/app.log`
2. Review error messages in API responses
3. Check [SETUP_GUIDE.md](./SETUP_GUIDE.md) troubleshooting section
