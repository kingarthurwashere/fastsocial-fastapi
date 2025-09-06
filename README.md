# FastSocial (FastAPI + Celery) — Daily Social Automation

This project reproduces the **Daily Social (Gemini + Canva → FB/IG/TikTok) + Email** workflow
in a scalable FastAPI service with Celery workers and Redis. It implements three scheduled slots
(**07:00**, **13:00**, **20:00** in `Africa/Harare` timezone) that:
1. Read today's row for the slot from Google Sheets (CSV publish or API).
2. Ask **Gemini 1.5 Flash** for a caption/hashtags and an `image_prompt`.
3. (Placeholder) Generate an image (Canva or your own generator), producing `image_url`.
4. Publish to Facebook Page, Instagram Business, TikTok (optional).
5. Email a delivery receipt.
6. Archive the JSON payload to local storage (optionally Google Drive).

> Minimal viable mode works with **published CSV** Google Sheet (no OAuth).
> For production, switch `GOOGLE_SHEETS_MODE=api` and wire a Service Account.

---

## Quick Start (Docker)

```bash
cp .env.example .env
# Fill your keys and IDs in .env

docker compose up --build
# API: http://localhost:8000
# Flower: http://localhost:5555  (Celery dashboard)
```

Manual triggers:
- `POST /trigger?slot=morning|afternoon|evening`

Health:
- `GET /healthz`

---

## Project Structure

```
app/
  celery_app.py
  config.py
  main.py
  schemas.py
  tasks.py
  utils/
    redis_lock.py
    time.py
  services/
    google_sheets.py
    gemini.py
    canva.py
    emailer.py
    drive.py
    publishers/
      facebook.py
      instagram.py
      tiktok.py
Dockerfile
docker-compose.yml
.env.example
pyproject.toml
```

---

## Notes

- Schedules mirror the n8n template (07:00, 13:00, 20:00 Africa/Harare).
- Each run is guarded by a Redis lock to avoid duplicate posting.
- Replace `CanvaService.generate_image` with your real Canva integration.
- Set `SHEETS_PUBLISHED_CSV_URL` if you prefer not to set up Google API yet.
- For Google API mode, place your service account JSON path in `GOOGLE_APPLICATION_CREDENTIALS`.

