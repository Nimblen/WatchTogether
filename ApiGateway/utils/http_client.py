import httpx
from fastapi import HTTPException

async def make_request(method: str, url: str, **kwargs):
    """
    Make a HTTP request
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, **kwargs)
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()