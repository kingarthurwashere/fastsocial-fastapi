import asyncio
from app.config import settings
from app.schemas import PlanRow, GeminiResult, PublishPayload, PublishResult, RunReport, TimeSlot
from app.services import google_sheets
from app.services.gemini import generate as gemini_generate
from app.services.canva import CanvaService
from app.services.publishers import facebook as fb_pub, instagram as ig_pub, tiktok as tt_pub
from app.services.emailer import send_email
from app.services.drive import archive_json

async def run_slot(slot: TimeSlot) -> RunReport:
    report = RunReport(slot=slot, errors=[])

    plan = google_sheets.read_today_slot(slot)
    if not plan:
        report.errors.append(f"No row for today/slot: {slot}")
        return report
    report.plan = plan

    gem: GeminiResult = await gemini_generate(plan)
    report.gemini = gem

    hashtags = ("#" + " #".join([h.strip("#") for h in gem.hashtags])) if gem.hashtags else ""
    content = (gem.caption or "").strip() + (f" {hashtags}" if hashtags else "")
    image_url = await CanvaService.generate_image(plan, gem)

    payload = PublishPayload(
        Date=plan.Date, TimeSlot=plan.TimeSlot, Topic=plan.Topic,
        content=content, image_url=image_url or "", video_url=""
    )
    report.payload = payload

    # Fan-out publishers
    fb_id = await fb_pub.publish(payload.content, payload.image_url or None)
    ig_id = await ig_pub.publish(payload.content, payload.image_url or None)
    tt_status = await tt_pub.publish(payload.content, payload.video_url or None)

    # Email
    html = f"""<h2>New Post Delivered</h2>
    <p><strong>Date:</strong> {payload.Date}</p>
    <p><strong>Time Slot:</strong> {payload.TimeSlot}</p>
    <p><strong>Topic:</strong> {payload.Topic}</p>
    <p><strong>Caption:</strong> {payload.content}</p>
    <p><strong>Image:</strong> {payload.image_url}</p>
    <p>✅ Published to Facebook, Instagram, TikTok.</p>
    """
    email_status = send_email(
        subject=f"Social Post Delivered – {payload.Topic} ({payload.TimeSlot})",
        html=html
    )

    # Archive
    archive_path = archive_json(
        filename_stem=f"{payload.Date}_{payload.TimeSlot}_{payload.Topic.replace(' ', '_')[:40]}",
        obj=payload.model_dump(),
    )

    report.result = PublishResult(
        facebook_id=fb_id, instagram_id=ig_id, tiktok_status=tt_status,
        email_status=email_status, archive_path=archive_path
    )
    return report
