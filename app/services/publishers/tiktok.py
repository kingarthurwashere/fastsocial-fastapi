from typing import Optional
import httpx
from app.config import settings

async def publish(caption: str, video_url: Optional[str]) -> Optional[str]:
    if not settings.TIKTOK_ACCESS_TOKEN:
        return None
    if not video_url:
        return None
    headers = {"Authorization": f"Bearer {settings.TIKTOK_ACCESS_TOKEN}"}
    async with httpx.AsyncClient(timeout=120.0, headers=headers) as client:
        r = await client.post(settings.TIKTOK_PUBLISH_URL, json={"video_url": video_url, "caption": caption})
        try:
            data = r.json()
            return data.get("status") or data.get("id")
        except Exception:
            return None
