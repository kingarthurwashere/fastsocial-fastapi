from typing import Optional
import httpx
from app.config import settings

# 1) Create media
CREATE_MEDIA_URL = "https://graph.facebook.com/v20.0/{ig_id}/media"
# 2) Publish media
PUBLISH_MEDIA_URL = "https://graph.facebook.com/v20.0/{ig_id}/media_publish"

async def publish(caption: str, image_url: Optional[str]) -> Optional[str]:
    if not settings.IG_ACCESS_TOKEN or not settings.IG_BUSINESS_ACCOUNT_ID:
        return None
    if not image_url:
        return None
    params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": settings.IG_ACCESS_TOKEN,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(CREATE_MEDIA_URL.format(ig_id=settings.IG_BUSINESS_ACCOUNT_ID), params=params)
        data = r.json()
        creation_id = data.get("id")
        if not creation_id:
            return None
        r2 = await client.post(PUBLISH_MEDIA_URL.format(ig_id=settings.IG_BUSINESS_ACCOUNT_ID), params={
            "creation_id": creation_id,
            "access_token": settings.IG_ACCESS_TOKEN
        })
        data2 = r2.json()
        return data2.get("id")
