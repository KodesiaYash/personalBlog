from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from boundary.connectors.blogs import Blogs
from boundary.connectors.categories import Categories
from boundary.connectors.mongoConnector import check_connection
import logging
import asyncio
from contextlib import asynccontextmanager
from bson import ObjectId
import traceback
import secrets
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Ensure environment variables are loaded
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Debugging statements
print(f"ADMIN_USERNAME: {ADMIN_USERNAME}")
print(f"ADMIN_PASSWORD: {ADMIN_PASSWORD}")

if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise ValueError("Environment variables ADMIN_USERNAME and ADMIN_PASSWORD must be set")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (use cautiously in production)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await check_connection()
    yield
    # Shutdown event (if needed)
    # Add any cleanup code here

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/getAllBlogs")
def get_all_blogs():
    blogs = Blogs()
    return {"allBlogs": blogs.list_blogs()}

class CategoryCreate(BaseModel):
    title: str
    description: str

@app.post("/createCategory")
async def create_category(category: CategoryCreate):
    logger.info("Creating category with provided data")
    try:
        categories = Categories()
        category_id = await categories.create_category(category.title, category.description)
        if category_id:
            return {"categoryId": category_id}  
        raise HTTPException(status_code=400, detail="Category creation failed")
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")

class BlogCreate(BaseModel):
    categoryId: str
    title: str
    content: str

@app.post("/createBlog")
async def create_blog(blog: BlogCreate):
    logger.info("Creating blog with provided data")
    try:
        blogs = Blogs()
        blog_id = await blogs.create_blog(blog.categoryId, blog.title, blog.content)
        if blog_id:
            return {"blogId": blog_id}  # No need to convert to string here
        raise HTTPException(status_code=400, detail="Blog creation failed")
    except Exception as e:
        logger.error(f"Error creating blog: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

@app.get("/admin", response_class=HTMLResponse)
async def admin_portal(request: Request, username: str = Depends(authenticate)):
    return templates.TemplateResponse("admin.html", {"request": request, "username": username})
