# ✅ EXECUTION CHECKLIST - Get Backend Running & Postman Setup

## 📍 Current Status
✅ Virtual Environment: Created  
✅ Dependencies: Installed  
✅ Backend Code: Ready  
❓ MongoDB: Needs configuration  
❓ Redis: Needs to be started  
❓ Backend Server: Not yet running  
❓ Postman: Not yet set up  

---

## 🎯 IMMEDIATE NEXT STEPS (Do These Now)

### STEP 1: Configure MongoDB (Choose One Option)

#### OPTION A: Use MongoDB Atlas (Recommended - Cloud Hosted)

**Time Required**: 10 minutes

1. **Go to** https://www.mongodb.com/cloud/atlas
2. **Sign up** (free account, no credit card needed)
3. **Create cluster**:
   - Choose "M0 Sandbox" (free tier)
   - Select AWS + us-east-1
   - Wait 2-5 minutes
4. **Create database user**:
   - Go to "Database Access"
   - Username: `emmi_user`
   - Password: Create strong password (e.g., `SecPass123!`)
   - Click "Add User"
5. **Allow network access**:
   - Go to "Network Access"
   - Click "Allow access from anywhere"
   - Confirm 0.0.0.0/0
6. **Get connection string**:
   - Go to "Databases"
   - Click "Connect"
   - Select "Drivers" → "Python"
   - Copy the connection string
   - It should look like:
     ```
     mongodb+srv://emmi_user:YourPassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```

7. **Update your .env file** with the connection string:
   - Replace the MONGODB_URL line with your actual connection string
   - Example:
     ```
     MONGODB_URL=mongodb+srv://emmi_user:SecPass123!@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
     ```

#### OPTION B: Use Local MongoDB (If Already Installed)

```bash
# Check if MongoDB is installed
which mongosh

# Start MongoDB
brew services start mongodb-community

# Verify
mongosh --eval "db.version()"
```

Update .env:
```
MONGODB_URL=mongodb://localhost:27017
```

---

### STEP 2: Start Redis

**Time Required**: 2 minutes

In a NEW terminal window:

```bash
# Option 1: Using Homebrew (if installed)
redis-server

# Option 2: If Homebrew not installed, use brew to install first
brew install redis
redis-server

# Option 3: Using Mac services
brew services start redis

# In another terminal, verify it's working
redis-cli ping
# Should return: PONG
```

**Keep this terminal open with Redis running**

---

### STEP 3: Start Backend Server

**Time Required**: 1 minute

In another NEW terminal window:

```bash
# Navigate to backend
cd /Users/emmidev/Desktop/Projects/PrimetradeAI_ProjectAssignment/backend

# Activate venv  
source venv/bin/activate

# Start server
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open**

---

### STEP 4: Verify Backend is Running

In yet ANOTHER terminal:

```bash
# Test health check
curl http://localhost:8000/

# Expected response:
# {"message":"Welcome to EmmiDev API"}
```

Or open in browser:
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Both should load successfully.

---

### STEP 5: Download & Setup Postman

**Time Required**: 5 minutes

1. **Download Postman**:
   - Go to https://www.postman.com/downloads/
   - Download for macOS
   - Install (drag to Applications)

2. **Open Postman**
   - Sign up with email (free)
   - Create new workspace: "EmmiDev API"
   - Create new collection: "EmmiDev API - v1"

3. **Set up Environment Variables**:
   - Click "Environments" → "Create Environment"
   - Name: "Local Development"
   - Add these variables:
     - `base_url` = `http://localhost:8000/api/v1`
     - `token` = (leave empty, will fill after login)
   - Click "Save"
   - Select this environment (top right dropdown)

---

## 🚀 QUICK TEST FLOW (Follow These Exact Steps)

### In Postman:

#### Request 1: Health Check
- **Method**: GET
- **URL**: `http://localhost:8000/`
- **Send** → Should see: `{"message":"Welcome to EmmiDev API"}`

#### Request 2: Register
- **Method**: POST
- **URL**: `{{base_url}}/auth/register`
- **Body** (raw JSON):
```json
{
  "email": "test@example.com",
  "password": "TestPassword123",
  "full_name": "Test User"
}
```
- **Send** → Should get 201 Created with user data

#### Request 3: Login
- **Method**: POST
- **URL**: `{{base_url}}/auth/login`
- **Body** (raw JSON):
```json
{
  "email": "test@example.com",
  "password": "TestPassword123"
}
```
- **Send** → Should get 200 OK with access_token
- **Copy the token value**

#### Request 4: Create Product
- **Method**: POST
- **URL**: `{{base_url}}/products/`
- **Headers**:
  - Key: `Authorization`
  - Value: `Bearer <paste-your-token-here>`
- **Body** (raw JSON):
```json
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics"
}
```
- **Send** → Should get 201 Created

#### Request 5: List Products
- **Method**: GET
- **URL**: `{{base_url}}/products/`
- **Headers**:
  - Key: `Authorization`
  - Value: `Bearer <paste-your-token-here>`
- **Send** → Should get 200 OK with product list

---

## ✅ SUCCESS INDICATORS

By the end, you should have:

- ✅ Terminal 1: Redis running (shows "Server started")
- ✅ Terminal 2: Backend running (shows "Uvicorn running on http://127.0.0.1:8000")
- ✅ Terminal 3: Can run curl commands successfully
- ✅ Browser: http://localhost:8000/docs loads with Swagger UI
- ✅ Postman: At least 5 requests working and returning correct responses
- ✅ No error messages in any terminals

---

## 🆘 TROUBLESHOOTING

### "Cannot connect to MongoDB"
- Verify MONGODB_URL in .env is correct
- Check MongoDB is running or Atlas is accessible
- Verify IP is whitelisted in MongoDB Atlas (Network Access)

### "Redis connection refused"
- Make sure redis-server is running in another terminal
- Try: `redis-cli ping` (should return PONG)
- If redis-cli not found: `brew install redis` then `redis-server`

### "Port 8000 already in use"
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### "ModuleNotFoundError"
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Swagger UI won't load
- Make sure backend is running: `uvicorn app.main:app --reload`
- Try in different browser
- Check http://localhost:8000/ works (health check)

---

## 📋 FINAL CHECKLIST

Before considering setup complete:

- [ ] MongoDB configured and connection string works
- [ ] Redis running and `redis-cli ping` returns PONG
- [ ] Backend running with no errors
- [ ] `curl http://localhost:8000/` returns welcome message
- [ ] Swagger UI loads at http://localhost:8000/docs
- [ ] Postman installed and configured
- [ ] All 5 test requests working in Postman
- [ ] Product list returns data from API
- [ ] Status: Ready to test with frontend

---

## 🎯 YOUR TODO RIGHT NOW

1. ⬜ Configure MongoDB (Atlas signup + get connection string)
2. ⬜ Update .env MONGODB_URL with your connection string
3. ⬜ Start Redis in terminal 1
4. ⬜ Start backend in terminal 2
5. ⬜ Test health check in terminal 3
6. ⬜ Install Postman
7. ⬜ Create workspace and collection
8. ⬜ Run all 5 test requests

**Estimated Total Time**: 20-30 minutes

---

## 💡 Pro Tips

- **Keep 3 terminals open**: Redis, Backend, Testing
- **Save responses** in Postman as examples
- **Auto-save token** by copying after login
- **Test caching** by running list request twice - second should be faster
- **Check logs** in backend terminal if errors occur

---

**Start with MongoDB setup above - come back here after each step completes! ⬆️**
