import os
from celery import Celery
from datetime import timedelta
from app.config import settings
from app.utils.redis_lock import acquire_lock, release_lock
from app.schemas import TimeSlot
import asyncio

celery_app = Celery(__name__, broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.conf.timezone = settings.TZ
celery_app.conf.accept_content = ["json"]
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"

# Schedule based on env (mirrors n8n cron slots)
celery_app.conf.beat_schedule = {
    "slot-morning": {
        "task": "app.celery_app.run_slot_task",
        "schedule": {"type": "crontab", "cron": settings.SLOT_CRON_MORNING},
        "args": ("morning",),
    },
    "slot-afternoon": {
        "task": "app.celery_app.run_slot_task",
        "schedule": {"type": "crontab", "cron": settings.SLOT_CRON_AFTERNOON},
        "args": ("afternoon",),
    },
    "slot-evening": {
        "task": "app.celery_app.run_slot_task",
        "schedule": {"type": "crontab", "cron": settings.SLOT_CRON_EVENING},
        "args": ("evening",),
    },
}

@celery_app.task(name="app.celery_app.run_slot_task")
def run_slot_task(slot: TimeSlot):
    key = f"lock:slot:{slot}"
    if not acquire_lock(key, ttl=600):  # 10 min lock
        return {"status": "skipped", "reason": "lock-not-acquired"}
    try:
        from app.tasks import run_slot
        res = asyncio.run(run_slot(slot))
        return res.model_dump()
    finally:
        release_lock(key)
