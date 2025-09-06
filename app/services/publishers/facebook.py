from typing import Optional
import httpx
from app.config import settings

FB_URL_TEMPLATE = "https://graph.facebook.com/v20.0/{page_id}/photos"

async def publish(message: str, image_url: Optional[str]) -> Optional[str]:
    if not settings.FB_PAGE_ACCESS_TOKEN or not settings.FB_PAGE_ID:
        return None
    params = {
        "caption": message,
        "access_token": settings.FB_PAGE_ACCESS_TOKEN,
    }
    if image_url:
        params["url"] = image_url
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(FB_URL_TEMPLATE.format(page_id=settings.FB_PAGE_ID), params=params)
        try:
            data = r.json()
            return data.get("id")
        except Exception:
            return None
