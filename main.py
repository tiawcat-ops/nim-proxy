from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NIM_API_KEY = os.environ["NIM_API_KEY"]
NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path: str, request: Request):
    body = await request.body()
    headers = {
        "Authorization": f"Bearer {NIM_API_KEY}",
        "Content-Type": "application/json",
    }

async with httpx.AsyncClient(timeout=120) as client:
    clean_path = path.lstrip("/")
    if clean_path.startswith("v1/"):
        clean_path = clean_path[3:]

    resp = await client.request(
        method=request.method,
        url=f"{NIM_BASE_URL}/{clean_path}",
        content=body,
        headers=headers,
    )
