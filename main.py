import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.endpoints.transaction_router as transaction_router
import app.endpoints.document_router as document_router

# App
app = FastAPI(title="Affidavit Mapp Dummy API")

# Configure logging
logger = logging.getLogger(__name__)


# Middleware
ALLOWED_ORIGINS = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Routes
@app.get('/', tags=["App"])
def index():
    return {"message": "Welcome to FastApi"}


app.include_router(transaction_router.router)
app.include_router(document_router.router)
