from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .apis.api import app
import uvicorn

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly include OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
