from fastapi import FastAPI

app = FastAPI(
    title="Perfume AI Ecommerce API",
    description="Backend for AI-powered perfume recommendation system",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Mabi Backend running"}