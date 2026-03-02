from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

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
        resp = await client.request(
            method=request.method,
            url=f"{NIM_BASE_URL}/{path}",
            content=body,
            headers=headers,
        )
    return resp.json()
