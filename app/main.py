import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.routers.perfume_router import router as perfume_router
from app.api.routers.ai_router import router as ai_router

load_dotenv()

app = FastAPI(
    title="Perfume AI Ecommerce API",
    description="Backend for AI-powered perfume recommendation system",
    version="1.0.0"
)

app.include_router(perfume_router)
app.include_router(ai_router)
@app.get("/")
def root():
    return {"message": "Mabi Backend running"}