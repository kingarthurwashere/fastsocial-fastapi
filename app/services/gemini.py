import httpx
from app.config import settings
from app.schemas import PlanRow, GeminiResult

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

async def generate(plan: PlanRow) -> GeminiResult:
    if not settings.GEMINI_API_KEY:
        return GeminiResult(caption="", hashtags=[], image_prompt=f"{plan.ImageStyle} illustration for: {plan.Topic}")
    prompt = (
        "Create platform-agnostic social captions and hashtags for topic: "
        f"{plan.Topic}. Keywords: {plan.Keywords}. CTA: {plan.CTA}. "
        "Return compact JSON with fields: caption, hashtags (array), image_prompt."
    )
    params = {"key": settings.GEMINI_API_KEY}
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(GEMINI_URL, params=params, json=body)
        text = ""
        try:
            data = r.json()
            cands = data.get("candidates", [])
            if cands and cands[0].get("content", {}).get("parts"):
                text = cands[0]["content"]["parts"][0].get("text", "")
        except Exception:
            text = ""

    # naive JSON extraction
    import re, json as pyjson
    parsed = {}
    try:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            parsed = pyjson.loads(m.group(0))
    except Exception:
        parsed = {}

    return GeminiResult(
        caption=parsed.get("caption", text or ""),
        hashtags=parsed.get("hashtags", []),
        image_prompt=parsed.get("image_prompt", f"{plan.ImageStyle} illustration for: {plan.Topic}"),
    )
