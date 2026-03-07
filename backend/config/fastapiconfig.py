from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import json
from typing import List


def create_configured_app() -> FastAPI:
    """
    Create and configure a FastAPI application
    """
    app = FastAPI()

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://localhost:5173", "http://localhost:3002"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


# Usage example:
"""
from fastapi import FastAPI, Request, Cookie
from pydantic import BaseModel

app = create_configured_app()

# Define a Pydantic model for request body (similar to bodyParser)
class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items")
async def create_item(item: Item, request: Request):
    # Access cookies
    cookies = request.cookies
    
    # Access headers
    auth_header = request.headers.get("x-access-token")
    
    return {"item": item, "cookies_received": cookies}

# For large file uploads (similar to 50mb limit)
@app.post("/upload")
async def upload_file(file: bytes = None):
    # Process file - FastAPI handles body parsing automatically
    return {"file_size": len(file) if file else 0}
"""
