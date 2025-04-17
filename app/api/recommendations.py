from datetime import datetime
from typing import Dict

from app.core.recommendations import generate_daily_recommendations_pdf
from app.utils.email_sender import send_pdf_via_email, send_startup_email
from config import settings
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/daily-recommendations-pdf")
async def send_daily_analytics_pdf() -> Dict[str, str]:
    try:
        await send_startup_email(subject="Daily Operational Insights - Startup")
        pdf_file = await generate_daily_recommendations_pdf()
        await send_pdf_via_email(
            pdf_data=pdf_file.getvalue(),
            subject=f"Daily Operational Insights of {datetime.now().strftime('%D')}",
        )
        return {"message": f"PDF sent successfully to {settings.REPORT_EMAIL_RECEIVER}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
