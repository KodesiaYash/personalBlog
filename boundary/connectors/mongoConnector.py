import os
import motor.motor_asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_USER = os.getenv("MONGO_DB_USER")
MONGO_DB_BLOG = os.getenv("MONGO_DB_BLOG")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
blogDB = client[MONGO_DB_BLOG]
userDB = client[MONGO_DB_USER]

async def check_connection():
    try:
        # The ping command is cheap and does not require auth.
        await client.admin.command('ping')
        print("MongoDB connection successful")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

async def start_session():
    return await client.start_session()


