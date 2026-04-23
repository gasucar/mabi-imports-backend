import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.routers.perfume_router import router as perfume_router
from app.api.routers.ai_router import router as ai_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.routers.seed_router import router as seed_router

load_dotenv()

app = FastAPI(
    title="Perfume AI Ecommerce API",
    description="Backend for AI-powered perfume recommendation system",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:5173")
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(perfume_router)
app.include_router(ai_router)
app.include_router(seed_router)
@app.get("/")
def root():
    return {"message": "Mabi Backend running"}