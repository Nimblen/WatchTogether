import httpx
import logging

logger = logging.getLogger(__name__)


class HTTPRequestError(Exception):
    def __init__(self, status_code: int = 500, detail: str = "Internal server error"):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP Request failed with status {status_code}: {detail}")


async def make_request(method: str, url: str, **kwargs):
    """
    Makes an HTTP request and handles errors gracefully.
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        logger.error(f"Request error for URL {url}: {exc}")
        raise HTTPRequestError(
            status_code=500, detail="Failed to connect to the service"
        )
    except httpx.HTTPStatusError as exc:
        logger.error(f"HTTP status error for URL {url}: {exc.response.text}")
        raise HTTPRequestError(
            status_code=exc.response.status_code, detail=exc.response.text
        )
    except Exception as exc:
        logger.error(f"Unexpected error for URL {url}: {exc}")
        raise HTTPRequestError(status_code=500, detail="An unexpected error occurred")
