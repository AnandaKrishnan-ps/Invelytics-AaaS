from email.message import EmailMessage
import aiosmtplib
from config import settings


async def send_pdf_via_email(
    pdf_data: bytes, subject: str, filename: str = "daily_recommendations.pdf"
) -> None:
    msg = EmailMessage()
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = settings.REPORT_EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.set_content("Please find attached the daily operational recommendations.")

    # Add PDF attachment
    msg.add_attachment(
        pdf_data, maintype="application", subtype="pdf", filename=filename
    )

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_SERVER,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )
