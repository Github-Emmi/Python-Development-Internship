# 🚀 Backend Setup & Postman Testing - Step-by-Step Guide

## ✅ Prerequisite Checklist

Before starting, verify you have:
- [ ] Python 3.9+ installed: `python3 --version`
- [ ] Access to MongoDB (Atlas account OR local installation)
- [ ] Redis installed or Docker available
- [ ] Backend folder accessible: `/Users/emmidev/Desktop/Projects/PrimetradeAI_ProjectAssignment/backend`
- [ ] .env file created in backend folder
- [ ] Postman installed (free from postman.com)

---

## PART 1: Backend Setup (Step-by-Step)

### Step 1: Navigate to Backend Directory

```bash
cd /Users/emmidev/Desktop/Projects/PrimetradeAI_ProjectAssignment/backend
pwd  # Verify you're in the right place
# Expected output: /Users/emmidev/Desktop/Projects/PrimetradeAI_ProjectAssignment/backend
```

### Step 2: Create Virtual Environment (If Not Exists)

```bash
# List directory to check if venv exists
ls -la | grep venv

# If venv doesn't exist, create it
python3 -m venv venv

# Verify venv was created
ls venv
```

### Step 3: Activate Virtual Environment

```bash
# Activate venv
source venv/bin/activate

# Verify activation (prompt should show (venv))
# Your terminal prompt should now show: (venv) $
which python
# Should output path ending in: venv/bin/python
```

### Step 4: Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Verify installation (should see list of packages)
pip list | grep -E "fastapi|motor|redis|pydantic|jose"
```

**Expected packages**:
- fastapi: 0.129.0
- motor: 3.7.1
- redis: 7.2.0
- pydantic: 2.12.5
- python-jose: 3.5.0
- passlib: 1.7.4
- bcrypt: 4.1.2

### Step 5: Verify .env File Exists

```bash
# Check if .env file exists
ls -la | grep env

# View current .env content
cat .env
```

**Expected content**:
```env
PROJECT_NAME=EmmiDev API
API_V1_STR=/api/v1
SECRET_KEY=your-super-secret-key-change-this-in-production
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
REDIS_URL=redis://localhost:6379
DATABASE_NAME=emmi_db
```

---

## PART 2: Setup External Services

### Option A: MongoDB Atlas (Cloud) - RECOMMENDED FOR TESTING

#### Step 1: Create MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Click "Start Free"
3. Sign up with email (or use Google/GitHub)
4. Accept terms and create account

#### Step 2: Create a Free Cluster

1. After login, click "Build a Database"
2. Choose **M0 Sandbox** (free tier)
3. Select cloud provider: **AWS**
4. Select region: **us-east-1** (or closest to you)
5. Click "Create Deployment"
6. Wait 2-5 minutes for cluster to be created

#### Step 3: Create Database User

1. Go to "Database Access" (left sidebar)
2. Click "Add New Database User"
3. Choose "Password" authentication
4. **Username**: `emmi_user`
5. **Password**: Create a strong password (save it!)
   - Example: `SecurePass123!AtlasDB`
6. Click "Add User"

#### Step 4: Configure Network Access

1. Go to "Network Access" (left sidebar)
2. Click "Add IP Address"
3. **For Development**: Click "Allow access from anywhere" (0.0.0.0/0)
   - ⚠️ NOT for production!
4. Click "Confirm"

#### Step 5: Get Connection String

1. Go to "Databases" (left sidebar)
2. Click "Connect" on your cluster
3. Choose "Drivers" → "Python"
4. Select version "5.9 or later"
5. Copy the connection string

**Example format**:
```
mongodb+srv://emmi_user:SecurePass123!AtlasDB@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

#### Step 6: Update .env File

```bash
# Edit .env file in your editor
nano .env
```

Or edit directly. Update these lines:

```env
MONGODB_URL=mongodb+srv://emmi_user:YOUR_PASSWORD@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=emmi_db
```

Save the file (Ctrl+O, Enter, Ctrl+X if using nano)

---

### Option B: MongoDB Local (If Already Installed)

```bash
# Start MongoDB
mongod

# In another terminal, verify connection
mongo
# Type: db.version()
# Exit with: exit()
```

Update .env:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=emmi_db
```

---

### Redis Setup (Choose One)

#### Option 1: Docker (Recommended for Mac)

```bash
# Start Redis in Docker
docker run -d -p 6379:6379 --name redis-emmidev redis:latest

# Verify Redis is running
docker ps | grep redis

# Test connection
redis-cli ping
# Should return: PONG
```

#### Option 2: Homebrew (If Installed)

```bash
# Install Redis (if not already installed)
brew install redis

# Start Redis
redis-server

# In another terminal, verify
redis-cli ping
# Should return: PONG
```

#### Option 3: Windows or Direct Install

Download from: https://github.com/microsoftarchive/redis/releases

**Verify .env has**:
```env
REDIS_URL=redis://localhost:6379
```

---

## PART 3: Start Backend Server

### Step 1: Verify All Services

```bash
# Terminal 1: Check Redis
redis-cli ping
# Expected: PONG

# Terminal 2: Check MongoDB connection string in .env
cat .env | grep MONGODB_URL
# Should show your connection string
```

### Step 2: Start FastAPI Server

```bash
# Make sure you're in the backend directory with venv activated
# Current directory: /Users/emmidev/Desktop/Projects/PrimetradeAI_ProjectAssignment/backend
# Prompt should show: (venv) $

# Start the server
uvicorn app.main:app --reload

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Don't close this terminal!** Keep it running while you test.

### Step 3: Verify Server is Running

Open a new terminal (keep the server running):

```bash
# Test basic connectivity
curl http://localhost:8000/

# Expected response:
# {"message":"Welcome to EmmiDev API"}
```

### Step 4: Access API Documentation

Open these URLs in your browser:

1. **Swagger UI (Interactive)**: http://localhost:8000/docs
   - This is where you can test endpoints directly
   - Should load with a blue header saying "Swagger UI"

2. **ReDoc (Beautiful Docs)**: http://localhost:8000/redoc
   - Alternative documentation view

If both load successfully, your backend is **running correctly**! ✅

---

## PART 4: Setup Postman (Complete Guide)

### Prerequisites
- Download Postman from: https://www.postman.com/downloads/
- Install and create free account
- No credit card required

### Step 1: Create Workspace

1. Open Postman
2. Click "Create Workspace" (top left)
3. **Workspace name**: `EmmiDev API`
4. **Visibility**: Personal
5. Click "Create Workspace"

### Step 2: Create API Collection

1. Click "+ Create" button
2. Select "Collection"
3. **Collection name**: `EmmiDev API - v1`
4. **Description**: Testing EmmiDev product API
5. Click "Create"

### Step 3: Add Environment Variables

1. Click "Environments" (left sidebar)
2. Click "+ Create Environment"
3. **Name**: `Local Development`

**Add these variables:**

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:8000/api/v1` | `http://localhost:8000/api/v1` |
| `token` | ` ` | (empty - will populate after login) |

4. Click "Save"

### Step 4: Select Environment

1. Top right, select "Local Development" from environment dropdown
2. Verify it shows the correct environment

---

## PART 5: Create Postman Requests

### Request 1: Health Check

**Request Details:**

1. Click "+ Add Request" in collection
2. **Request name**: `01 - Health Check`
3. **Method**: GET
4. **URL**: `{{base_url}}/..` 

Wait, let me correct - the health check is at the root:

```
http://localhost:8000/
```

**Steps**:
1. Name: `01 - Health Check`
2. Method: GET
3. URL: `http://localhost:8000/`
4. Click "Send"

**Expected Response** (200 OK):
```json
{
  "message": "Welcome to EmmiDev API"
}
```

---

### Request 2: Register User

**Request Details:**

1. Click "+ Add Request"
2. **Name**: `02 - Register User`
3. **Method**: POST
4. **URL**: `{{base_url}}/auth/register`

**Headers Tab:**
```
Content-Type: application/json
```
(Usually auto-added)

**Body Tab:**
- Select "raw"
- Select "JSON" from dropdown
- Add this JSON:

```json
{
  "email": "testuser@example.com",
  "password": "TestPassword123",
  "full_name": "Test User"
}
```

**Click "Send"**

**Expected Response** (201 Created):
```json
{
  "id": "507f1f77bcf86cd799439011",
  "_id": "507f1f77bcf86cd799439011",
  "email": "testuser@example.com",
  "full_name": "Test User",
  "is_active": true
}
```

---

### Request 3: Login User

**Request Details:**

1. Click "+ Add Request"
2. **Name**: `03 - Login User`
3. **Method**: POST  
4. **URL**: `{{base_url}}/auth/login`

**Body** (raw JSON):
```json
{
  "email": "testuser@example.com",
  "password": "TestPassword123"
}
```

**Click "Send"**

**Expected Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "507f1f77bcf86cd799439011"
}
```

**IMPORTANT**: Copy the `access_token` value

### Update Environment Variable with Token

1. Click "Environments" → "Local Development"
2. Find `token` variable
3. Paste the token value in "Current Value" field
4. Click "Save"

Save the response value as token. Use these steps:

**Option A: Manual**
1. Copy `access_token` value from response
2. Click Environments → Local Development
3. Set `token` variable = your copied token
4. Save

**Option B: Automatic (Tests)**
1. Go to "Tests" tab in login request
2. Add this code:

```javascript
if (pm.response.code === 200) {
    pm.environment.set("token", pm.response.json().access_token);
}
```

3. Now token auto-saves after login

---

### Request 4: Create Product

**Request Details:**

1. Click "+ Add Request"
2. **Name**: `04 - Create Product`
3. **Method**: POST
4. **URL**: `{{base_url}}/products/`

**Headers Tab:**
- Key: `Authorization`
- Value: `Bearer {{token}}`

**Body** (raw JSON):
```json
{
  "name": "Premium Laptop",
  "price": 1299.99,
  "category": "Electronics"
}
```

**Click "Send"**

**Expected Response** (201 Created):
```json
{
  "id": "507f1f77bcf86cd799439012",
  "_id": "507f1f77bcf86cd799439012",
  "name": "Premium Laptop",
  "price": 1299.99,
  "category": "Electronics"
}
```

Save the returned `id` value - you'll need it for other requests.

---

### Request 5: List Products (Get All)

**Request Details:**

1. Click "+ Add Request"
2. **Name**: `05 - List Products`
3. **Method**: GET
4. **URL**: `{{base_url}}/products/?skip=0&limit=10`

**Headers:**
- Key: `Authorization`
- Value: `Bearer {{token}}`

**Click "Send"**

**Expected Response** (200 OK):
```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "_id": "507f1f77bcf86cd799439012",
    "name": "Premium Laptop",
    "price": 1299.99,
    "category": "Electronics"
  }
]
```

**Performance Note**: 
- First request hits MongoDB (slower)
- Second request (within 5 min) hits Redis cache (instant!)
- Click Send again within 5 minutes to see speed difference

---

### Request 6: Get Single Product

**Request Details:**

1. Click "+ Add Request"
2. **Name**: `06 - Get Product by ID`
3. **Method**: GET
4. **URL**: `{{base_url}}/products/507f1f77bcf86cd799439012`
   - Replace ID with your product's ID from Request 4

**Headers:**
- Key: `Authorization`
- Value: `Bearer {{token}}`

**Click "Send"**

**Expected Response** (200 OK):
```json
{
  "id": "507f1f77bcf86cd799439012",
  "_id": "507f1f77bcf86cd799439012",
  "name": "Premium Laptop",
  "price": 1299.99,
  "category": "Electronics"
}
```

---

### Request 7: Update Product

**Request Details:**

1. Click "+ Add Request"
2. **Name**: `07 - Update Product`
3. **Method**: PUT
4. **URL**: `{{base_url}}/products/507f1f77bcf86cd799439012`
   - Replace ID with your product's ID

**Headers:**
- Key: `Authorization`
- Value: `Bearer {{token}}`

**Body** (raw JSON) - only changed fields:
```json
{
  "price": 999.99,
  "category": "Computers"
}
```

**Click "Send"**

**Expected Response** (200 OK):
```json
{
  "id": "507f1f77bcf86cd799439012",
  "_id": "507f1f77bcf86cd799439012",
  "name": "Premium Laptop",
  "price": 999.99,
  "category": "Computers"
}
```

---

### Request 8: Delete Product

**Request Details:**

1. Click "+ Add Request"
2. **Name**: `08 - Delete Product`
3. **Method**: DELETE
4. **URL**: `{{base_url}}/products/507f1f77bcf86cd799439012`
   - Replace ID with your product's ID

**Headers:**
- Key: `Authorization`
- Value: `Bearer {{token}}`

**Click "Send"**

**Expected Response** (204 No Content):
- Empty response body
- Status: 204

---

## PART 6: Complete Testing Flow in Postman

### Run Complete Test Suite

1. **Health Check** (No auth needed)
   - Request 1: GET `http://localhost:8000/`
   - Expected: 200 OK, welcome message

2. **Register New User** (No auth needed)
   - Request 2: POST `/auth/register`
   - Provide: email, password, full_name
   - Expected: 201 Created with user data

3. **Login** (No auth needed)
   - Request 3: POST `/auth/login`
   - Provide: email, password
   - Expected: 200 OK with JWT token
   - **Action**: Copy token to environment variable

4. **Create Product** (Auth required)
   - Request 4: POST `/products/`
   - Headers: Include Authorization bearer token
   - Provide: name, price, category
   - Expected: 201 Created with product data
   - **Action**: Save product ID

5. **List Products** (Auth required)
   - Request 5: GET `/products/?skip=0&limit=10`
   - Headers: Include Authorization bearer token
   - Expected: 200 OK with array of products
   - **Note**: Try twice - compare speed (cache feature)

6. **Get Single Product** (Auth required)
   - Request 6: GET `/products/{id}`
   - Use product ID from Request 4
   - Expected: 200 OK with single product

7. **Update Product** (Auth required)
   - Request 7: PUT `/products/{id}`
   - Update price or category
   - Expected: 200 OK with updated data

8. **Delete Product** (Auth required)
   - Request 8: DELETE `/products/{id}`
   - Expected: 204 No Content

---

## PART 7: Postman Tips & Tricks

### Save Responses

Right after any request, click "Save Response" → "Save as example"
- Useful for documentation
- Shows expected outputs

### Pre-request Scripts

Before login request, add to "Pre-request Script" tab:

```javascript
// Clear old token
pm.environment.set("token", "");
```

### Test Scripts (Auto-validation)

In "Tests" tab of each request:

```javascript
// For POST requests expecting 201
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

// For GET requests expecting 200
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Validate response has expected fields
pm.test("Response has email field", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('email');
});
```

### Collection Runner (Test All at Once)

1. Click "Collection Runner" (top left, play icon)
2. Select your collection
3. Select environment "Local Development"
4. Click "Run"
5. Watch all requests execute automatically

### Export Collection

1. Right-click collection
2. Select "Export"
3. Save as JSON file
4. Share with team or backup

---

## PART 8: Troubleshooting

### Error: "Cannot GET /api/v1/auth/login"

**Cause**: Backend not running
**Solution**: 
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Error: "Failed to fetch" / "Connection refused"

**Cause**: Backend not listening on port 8000
**Solution**:
1. Check backend terminal for errors
2. Try: `curl http://localhost:8000/`
3. Verify firewall isn't blocking

### Error: "401 Unauthorized"

**Cause**: Missing or invalid token
**Solution**:
1. Make sure you logged in (Request 3)
2. Copy token to environment variable
3. Verify header has: `Authorization: Bearer {{token}}`

### Error: "404 Not Found" for product

**Cause**: Wrong product ID
**Solution**:
1. Get fresh product ID from create request
2. Replace in URL exactly as returned

### Error: "MongoDB connection error"

**Cause**: Connection string wrong or service down
**Solution**:
1. Check .env MONGODB_URL is correct
2. Verify MongoDB is running (Atlas or local)
3. Check IP whitelist in MongoDB Atlas

### Error: "Redis connection error"

**Cause**: Redis not running
**Solution**:
1. Start Redis: `redis-server` or `docker run...`
2. Test: `redis-cli ping`
3. Should return: PONG

---

## PART 9: Performance Testing

### Test Redis Caching

1. Create a product (Request 4)
2. List products (Request 5)
   - **Note response time** - should be ~500ms (first request)
3. Click Send again immediately
   - **Note response time** - should be <100ms (cached!)
4. Create another product (clears cache)
5. List products again
   - Should be ~500ms again (cache was invalidated)

### Expected Performance

| Operation | First Time | Cached |
|-----------|-----------|--------|
| List products | 300-500ms | <100ms |
| Get single product | 50-150ms | 50-150ms |
| Create product | 100-300ms | 100-300ms |
| Update product | 100-300ms | 100-300ms |
| Delete product | 100-300ms | 100-300ms |

---

## PART 10: Next Steps

### ✅ Completion Checklist

After following all these steps:

- [ ] Backend running on http://localhost:8000
- [ ] API docs loading at http://localhost:8000/docs
- [ ] Postman workspace created
- [ ] Environment configured with base_url and token
- [ ] All 8 requests set up and working
- [ ] Testing flow completed successfully
- [ ] Responses match expected formats
- [ ] Token auto-saves to environment
- [ ] Caching performance verified
- [ ] Error handling tested

### 🚀 What's Next?

1. **Test with frontend**: Start frontend dev server
   - `cd frontend && npm run dev`
   
2. **Try more scenarios**:
   - Register multiple users
   - Create multiple products
   - Update and delete operations
   - Test error cases

3. **Load Testing**:
   - Create many products
   - List with high pagination
   - Monitor backend logs

4. **Production Ready**:
   - Update SECRET_KEY in .env
   - Change MongoDB connection for prod
   - Review security settings

---

## Quick Reference: All Endpoints

```
GET    http://localhost:8000/
POST   http://localhost:8000/api/v1/auth/register
POST   http://localhost:8000/api/v1/auth/login
POST   http://localhost:8000/api/v1/products/
GET    http://localhost:8000/api/v1/products/
GET    http://localhost:8000/api/v1/products/{id}
PUT    http://localhost:8000/api/v1/products/{id}
DELETE http://localhost:8000/api/v1/products/{id}
```

---

**All set! You're ready to test the API with Postman! 🎉**

For any issues, check the troubleshooting section above.
