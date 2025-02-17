from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .apis.api import app
import uvicorn

# Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],  # Explicitly include OPTIONS
#     allow_headers=["*"],
#     expose_headers=["*"],
#     max_age=600,  # Cache preflight requests for 10 minutes
# )

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
if __name__ == "__main__":
    uvicorn.run(app, host="VM-021-SPA.NITORINFOTECH.IN", port=8001)