from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal, Dict, Any

TimeSlot = Literal["morning", "afternoon", "evening"]

class PlanRow(BaseModel):
    Date: str
    TimeSlot: TimeSlot
    Topic: str = ""
    Keywords: str = ""
    CTA: str = ""
    ImageStyle: str = ""

class GeminiResult(BaseModel):
    caption: str = ""
    hashtags: List[str] = []
    image_prompt: str = ""

class PublishPayload(BaseModel):
    Date: str
    TimeSlot: TimeSlot
    Topic: str
    content: str
    image_url: Optional[str] = ""
    video_url: Optional[str] = ""

class PublishResult(BaseModel):
    facebook_id: Optional[str] = None
    instagram_id: Optional[str] = None
    tiktok_status: Optional[str] = None
    email_status: Optional[str] = None
    archive_path: Optional[str] = None

class RunReport(BaseModel):
    slot: TimeSlot
    plan: Optional[PlanRow] = None
    gemini: Optional[GeminiResult] = None
    payload: Optional[PublishPayload] = None
    result: Optional[PublishResult] = None
    errors: List[str] = []
