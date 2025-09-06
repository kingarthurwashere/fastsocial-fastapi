from fastapi import FastAPI, HTTPException, Query
from app.config import settings
from app.schemas import RunReport, TimeSlot
from app.celery_app import run_slot_task

app = FastAPI(title="FastSocial API", version="0.1.0")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "env": settings.ENV, "tz": settings.TZ}

@app.post("/trigger", response_model=dict)
def trigger(slot: TimeSlot = Query(..., description="morning | afternoon | evening")):
    task = run_slot_task.delay(slot)
    return {"task_id": task.id, "slot": slot}
