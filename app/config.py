from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, case_sensitive=False)

    ENV: str = "dev"
    TZ: str = "Africa/Harare"
    LOG_LEVEL: str = "INFO"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    REDIS_URL: str = "redis://redis:6379/0"

    SLOT_CRON_MORNING: str = "0 7 * * *"
    SLOT_CRON_AFTERNOON: str = "0 13 * * *"
    SLOT_CRON_EVENING: str = "0 20 * * *"

    GOOGLE_SHEETS_MODE: str = "csv"  # csv | api
    SHEETS_PUBLISHED_CSV_URL: Optional[str] = None
    SHEETS_CONTENT_RANGE: str = "ContentPlan!A:F"

    SHEETS_DATE_COLUMN: str = "Date"
    SHEETS_TIMESLOT_COLUMN: str = "TimeSlot"
    SHEETS_TOPIC_COLUMN: str = "Topic"
    SHEETS_KEYWORDS_COLUMN: str = "Keywords"
    SHEETS_CTA_COLUMN: str = "CTA"
    SHEETS_IMAGESTYLE_COLUMN: str = "ImageStyle"

    GOOGLE_SHEET_ID: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None

    GEMINI_API_KEY: Optional[str] = None

    FB_PAGE_ACCESS_TOKEN: Optional[str] = None
    FB_PAGE_ID: Optional[str] = None

    IG_ACCESS_TOKEN: Optional[str] = None
    IG_BUSINESS_ACCOUNT_ID: Optional[str] = None

    TIKTOK_ACCESS_TOKEN: Optional[str] = None
    TIKTOK_PUBLISH_URL: str = "https://open.tiktokapis.com/v2/post/publish/"

    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@example.com"
    EMAIL_TO: str = "you@example.com"

    ARCHIVE_DIR: str = "/data/archives"

settings = Settings()
