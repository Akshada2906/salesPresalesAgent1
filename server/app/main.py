from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .apis.api import app
import uvicorn

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
