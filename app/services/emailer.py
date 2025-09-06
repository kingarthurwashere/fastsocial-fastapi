import smtplib
from email.mime.text import MIMEText
from typing import Optional
from app.config import settings

def send_email(subject: str, html: str) -> Optional[str]:
    if not settings.SMTP_HOST:
        return None
    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = settings.EMAIL_TO
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD or "")
            server.sendmail(settings.EMAIL_FROM, [settings.EMAIL_TO], msg.as_string())
        return "sent"
    except Exception:
        return None
