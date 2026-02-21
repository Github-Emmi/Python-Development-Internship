import logging
import os
import sys
import time
import random
from datetime import datetime

# Ensure we can import from app
sys.path.append(os.getcwd())

try:
    from app.core.logging import setup_logging
except ImportError:
    print("Error: Could not import app.core.logging. Make sure you are in the 'backend' directory.")
    sys.exit(1)

def generate_logs():
    # Setup logging (creates logs/app.log and logs/error.log)
    logger = setup_logging()
    
    # Define sample data
    users = ["joydip@primetrade.ai", "hello@primetrade.ai", "chetan@primetrade.ai", "sonika@primetrade.ai", "emmidev@example.com"]
    products = ["Bitcoin Miner S19", "Ledger Nano X", "Trezor Model T", "NVIDIA RTX 4090", "Trading Bot Subscription"]
    
    print("Generating realistic logs...")
    
    # 1. Startup Sequence
    logger.info("Loading configuration...")
    logger.info("Connecting to MongoDB...")
    time.sleep(0.1)
    logger.info("Connection to MongoDB established successfully.")
    logger.info("Connecting to Redis...")
    time.sleep(0.1)
    logger.info("Redis connection established.")
    logger.info("Application startup complete. Uvicorn running on http://127.0.0.1:8000")
    
    # 2. Simulate User Activity
    for i in range(15):
        user = random.choice(users)
        action = random.choice(["login", "register", "view_products", "view_products", "create_product", "update_product", "error"])
        
        if action == "register":
            logger.info(f"Registering new user: {user}")
            logger.info(f"User registered successfully: {user}")
            
        elif action == "login":
            logger.info(f"User login attempt: {user}")
            logger.info(f"User logged in successfully: {user}")
            
        elif action == "view_products":
            # Simulate cache hit/miss
            if random.random() > 0.3:
                logger.info(f"Cache hit for products_list:skip:0:limit:10")
            else:
                logger.info(f"Cache miss for products_list:skip:0:limit:10 - fetching from MongoDB")
                
        elif action == "create_product":
            product = random.choice(products)
            logger.info(f"Product created by {user}: {product}")
            logger.info("Product created successfully with ID: 65d6a7b8f9e0c1d2e3f4a5b6")
            logger.info("Invalidating cache key: products_list")
            
        elif action == "update_product":
            product_id = "507f1f77bcf86cd79943901" + str(random.randint(0, 9))
            logger.info(f"Product {product_id} updated by admin {user}")
            logger.info("Invalidating cache key: products_list")
            
        elif action == "error":
            # Simulate an error
            product_id = "invalid_id_" + str(random.randint(100, 999))
            logger.error(f"Error fetching product {product_id}: Product not found")
                
    # 3. Shutdown Sequence
    logger.info("Shutting down application...")
    logger.info("Closing MongoDB connection...")
    logger.info("Closing Redis connection...")
    logger.info("Application shutdown complete.")
    
    print(f"✅ Logs generated successfully in {os.getcwd()}/logs/")

if __name__ == "__main__":
    generate_logs()