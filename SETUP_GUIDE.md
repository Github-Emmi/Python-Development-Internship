# EmmiDev API - Backend Setup Guide

## 🚀 Quick Start

### Phase 1: Environment Setup

#### 1. Activate Python Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

#### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

#### 3. Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your actual values
nano .env
```

**Required environment variables:**
- `SECRET_KEY`: Generate a secure key for JWT tokens
- `MONGODB_URL`: Your MongoDB Atlas connection string
- `REDIS_URL`: Your Redis connection string (localhost for development)

---

## 📊 MongoDB Atlas Setup Guide

### Step 1: Create a MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Start Free" or sign in if you have an account
3. Create a new account or use existing credentials

### Step 2: Create a New Project

1. Click "Create a Project"
2. Enter project name: `EmmiDev`
3. Click "Create Project"

### Step 3: Create a Database Cluster

1. Click "Build a Database"
2. Choose **M0 Sandbox** (free tier)
3. Select your cloud provider and region (choose closest to you)
4. Click "Create Deployment"

### Step 4: Configure Database Access

1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Enter username: `emmi_user`
5. Enter a strong password
6. Click "Add User"

**Save your username and password - you'll need them for the connection string**

### Step 5: Configure Network Access

1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
4. Click "Confirm"

### Step 6: Get Connection String

1. Go back to "Databases" overview
2. Click "Connect" on your cluster
3. Choose "Drivers"
4. Select "Node.js" and version "5.9 or later"
5. Copy the connection string

**Example format:**
```
mongodb+srv://emmi_user:yourpassword@cluster.mongodb.net/?retryWrites=true&w=majority
```

6. Replace placeholders:
   - `emmi_user` with your database username
   - `yourpassword` with your database password
   - Remove `/<database>` at the end (it will auto-select)

### Step 7: Update .env

```env
MONGODB_URL=mongodb+srv://emmi_user:yourpassword@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=emmi_db
```

---

## 🔴 Redis Setup (Local Development)

### Option 1: Using Docker (Recommended)

```bash
# Start Redis container
docker run -d -p 6379:6379 --name redis-emmi redis:latest

# Verify it's running
redis-cli ping
# Should return: PONG
```

### Option 2: MacOS (Homebrew)

```bash
# Install Redis
brew install redis

# Start Redis service
redis-server

# In another terminal, verify
redis-cli ping
# Should return: PONG
```

### Option 3: Windows

1. Download Redis from [Github Releases](https://github.com/microsoftarchive/redis/releases)
2. Install the MSI file
3. Redis runs as a Windows service automatically

---

## 🏃 Running the Backend

### Start the Server

```bash
# From backend directory with venv activated
uvicorn app.main:app --reload

# The server will start at http://localhost:8000
```

### Test the API

Open your browser and go to:
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

---

## 📡 API Endpoints Overview

### Authentication Endpoints
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Product Endpoints (with Redis Caching)
- `POST /api/v1/products/` - Create a product
- `GET /api/v1/products/` - List all products (cached for 5 min)
- `GET /api/v1/products/{product_id}` - Get product details
- `PUT /api/v1/products/{product_id}` - Update a product
- `DELETE /api/v1/products/{product_id}` - Delete a product

---

## 🧪 Testing the API with cURL

### Register User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Create Product

```bash
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Premium Laptop",
    "price": 1299.99,
    "category": "Electronics"
  }'
```

### Get All Products (with Caching)

```bash
curl http://localhost:8000/api/v1/products/
```

First request hits MongoDB, subsequent requests (within 5 min) are served from Redis cache.

---

## 🐛 Troubleshooting

### MongoDB Connection Failed
- Verify IP is whitelisted in MongoDB Atlas > Network Access
- Check username and password in MONGODB_URL
- Ensure database exists in MongoDB Atlas

### Redis Connection Failed
- Make sure Redis is running: `redis-cli ping`
- Check Redis is on localhost:6379
- For Docker: `docker ps` to see if container is running

### ModuleNotFoundError
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version: `python --version` (should be 3.9+)

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py        # Authentication routes
│   │   │   └── items.py       # Product CRUD routes
│   │   └── v1/
│   │       └── api.py         # API router aggregator
│   ├── core/
│   │   ├── config.py          # Settings
│   │   ├── security.py        # JWT & password hashing
│   │   └── logging.py         # Logging configuration
│   ├── db/
│   │   ├── mongodb.py         # MongoDB connection
│   │   └── redis.py           # Redis connection
│   ├── models/
│   │   ├── common.py          # PyObjectId for BSON
│   │   ├── user.py            # User model
│   │   └── product.py         # Product model
│   ├── schemas/
│   │   ├── user.py            # User validation schemas
│   │   └── product.py         # Product validation schemas
│   └── services/
│       ├── auth.py            # Auth business logic
│       └── product_service.py # Product CRUD logic
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

---

## 🔒 Security Best Practices

1. **Never commit .env** - Add to `.gitignore`
2. **Rotate SECRET_KEY** in production
3. **Use HTTPS** in production
4. **Limit CORS origins** - Update in main.py for production
5. **Use strong passwords** for MongoDB
6. **Enable IP whitelisting** in MongoDB Atlas

---

## 🎯 Next Steps

1. ✅ Setup environment and dependencies
2. ✅ Configure MongoDB Atlas
3. ✅ Setup local Redis
4. ✅ Run backend server
5. 🔄 **Frontend Setup** (Next phase: Vite + React + Shadcn UI)

---

For questions or issues, check the [Troubleshooting](#troubleshooting) section or review logs in `logs/app.log`.
