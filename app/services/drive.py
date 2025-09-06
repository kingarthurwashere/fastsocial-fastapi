import json, os
from typing import Optional
from app.config import settings

def archive_json(filename_stem: str, obj) -> Optional[str]:
    os.makedirs(settings.ARCHIVE_DIR, exist_ok=True)
    path = os.path.join(settings.ARCHIVE_DIR, f"{filename_stem}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path
