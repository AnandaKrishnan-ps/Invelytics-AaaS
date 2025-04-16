from typing import Dict
from app.core.recommendations import generate_daily_recommendations_pdf
from app.utils.email_sender import send_pdf_via_email
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/daily-recommendations-pdf")
async def send_daily_analytics_pdf() -> Dict[str, str]:
    try:
        pdf_file = await generate_daily_recommendations_pdf()
        await send_pdf_via_email(
            pdf_data=pdf_file.getvalue(), subject="Daily Operational Insights 📊"
        )
        return {"message": "PDF sent via email ✅"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
