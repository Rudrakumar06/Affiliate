from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from pathlib import Path
import logging

# Import route modules
from .routes.products import router as products_router
from .routes.categories import router as categories_router
from .routes.testimonials import router as testimonials_router
from .routes.data_seeder import router as seeder_router
from .database import close_database_connection

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Affiliate Marketing API", version="1.0.0")

# Include routers with /api prefix
app.include_router(products_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(testimonials_router, prefix="/api")
app.include_router(seeder_router, prefix="/api")

# Root endpoint
@app.get("/api/")
async def root():
    return {"message": "Affiliate Marketing API is running!", "version": "1.0.0"}

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "affiliate-marketing-api"}

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Affiliate Marketing API...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Affiliate Marketing API...")
    await close_database_connection()