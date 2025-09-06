import csv, io, httpx
from typing import List, Optional
from app.config import settings
from app.schemas import PlanRow, TimeSlot
from app.utils.time import today_iso

def _read_csv_rows(url: str) -> List[dict]:
    resp = httpx.get(url, timeout=30.0)
    resp.raise_for_status()
    content = resp.text
    reader = csv.DictReader(io.StringIO(content))
    return list(reader)

def read_today_slot(slot: TimeSlot) -> Optional[PlanRow]:
    """Reads today's row for the slot. CSV mode for simplicity.
    You can replace this with Google API mode when ready.
    """
    if settings.GOOGLE_SHEETS_MODE == "csv":
        if not settings.SHEETS_PUBLISHED_CSV_URL:
            return None
        rows = _read_csv_rows(settings.SHEETS_PUBLISHED_CSV_URL)
    else:
        # TODO: Implement Google Sheets API mode
        # Left as an exercise (gspread + service account)
        return None

    today = today_iso(settings.TZ)
    date_col = settings.SHEETS_DATE_COLUMN
    slot_col = settings.SHEETS_TIMESLOT_COLUMN
    get = lambda r, k: (r.get(k) or r.get(k.lower()) or r.get(k.upper()) or "").strip()

    for r in rows:
        d = get(r, date_col)[:10]
        s = get(r, slot_col).lower()
        if d == today and s == slot:
            return PlanRow(
                Date=d,
                TimeSlot=slot,
                Topic=get(r, settings.SHEETS_TOPIC_COLUMN),
                Keywords=get(r, settings.SHEETS_KEYWORDS_COLUMN),
                CTA=get(r, settings.SHEETS_CTA_COLUMN),
                ImageStyle=get(r, settings.SHEETS_IMAGESTYLE_COLUMN),
            )
    return None
