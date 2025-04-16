from core.recommendations import generate_daily_recommendations_pdf
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/daily-recommendations-pdf")
async def get_daily_recommendations_pdf():
    """
    Endpoint to generate and download a PDF with daily operational insights.
    Returns the PDF as a downloadable file.
    """
    try:
        pdf_file = await generate_daily_recommendations_pdf()
        return StreamingResponse(
            pdf_file,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=daily_recommendations.pdf"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
