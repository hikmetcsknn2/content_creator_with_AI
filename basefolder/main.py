"""
Content Assistant API - Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

# FastAPI app oluştur
app = FastAPI(
    title="Content Assistant API",
    description="AI-powered content generation system",
    version="2.0.0"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route'ları ekle
app.include_router(router)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Content Assistant API v2.0", "status": "running"}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)