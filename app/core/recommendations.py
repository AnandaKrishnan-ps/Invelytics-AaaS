import asyncio
import io
from datetime import datetime
from typing import List

from app.core.inventory_logic import get_all_inventory_items
from app.core.logs import get_logs_service
from app.core.prompts import (
    get_analytics_prompt,
    get_combined_prompt,
    get_recommendations_prompt,
)
from app.db.database import Database
from app.models.inventory_schema import InventoryResponse
from app.models.logs_schema import InventoryLogResponse
from ollama import AsyncClient
from xhtml2pdf import pisa  # type: ignore

OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"


def compress_inventory(inventory: List[InventoryResponse]) -> str:
    """Compress inventory into a token-efficient summary."""
    return ", ".join(
        [
            f"{item.name} - {item.quantity} units of {item.category or 'Miscellaneous'} - last updated on {item.last_updated.strftime('%D')}"
            for item in inventory
        ]
    )


def compress_log(logs: List[InventoryLogResponse]) -> str:
    return ", ".join(
        [
            f"item id \"{log.item_id}\" - \"Category\" - {log.category} - OLD QUANTITY => {log.old_quantity}; NEW QUANTITY => {log.updated_quantity}, updated on {log.date.strftime('%D')}"
            for log in logs
        ]
    )


async def call_ollama(prompt: str, system: str = "") -> str:
    try:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]

        response = await AsyncClient().chat(
            model=OLLAMA_MODEL, messages=messages, stream=False
        )

        curated_response = response.message.content

        if not curated_response:
            raise ValueError("Empty response from Ollama API")

        return curated_response

    except Exception as e:
        raise ValueError(f"Error calling Ollama API: {e}")


async def generate_html_report(
    inventory: List[InventoryResponse], logs: List[InventoryLogResponse]
) -> str:
    """Pipeline to create the complete HTML report."""
    today = datetime.now().strftime("%Y-%m-%d")
    inventory_summary = compress_inventory(inventory)
    logs_summary = compress_log(logs)

    analytics_prompt = get_analytics_prompt(today, inventory_summary, logs_summary)
    recommendation_prompt = get_recommendations_prompt(
        today, inventory_summary, logs_summary
    )

    analytics_response, recommendation_response = await asyncio.gather(
        call_ollama(
            analytics_prompt,
            system="You write professional business analytics reports.",
        ),
        call_ollama(
            recommendation_prompt,
            system="You are a strategic advisor that outputs business suggestions.",
        ),
    )

    combined_prompt = get_combined_prompt(
        today, analytics_response, recommendation_response
    )

    combined_response = await call_ollama(
        combined_prompt,
        system="You are a business analyst AI that combines reports.",
    )

    return f"""
    <html>
        <head><title>Daily Inventory Report - {today}</title></head>
        <body>
            <h1>Daily Inventory Report</h1>
            <h2>Date: {today}</h2>
            <hr/>
            {combined_response}
            <hr/>
        </body>
    </html>
    """


async def generate_daily_recommendations_pdf() -> io.BytesIO:
    """Master function to create final PDF."""
    try:
        inventory = await get_all_inventory_items(
            Database._db.inventory,
            limit=50,
            skip=0,
            sort_by="last_updated",
            sort_order="desc",
        )
        inventory.sort(key=lambda item: item.last_updated, reverse=True)

        logs = await get_logs_service(
            Database._db.inventory_logs,
            limit=50,
            offset=0,
            sort_by="date",
            sort_order="desc",
        )
        logs.sort(key=lambda item: item.date, reverse=True)

        html_content = await generate_html_report(inventory, logs)

        # Convert to PDF
        pdf_buffer = io.BytesIO()
        pisa.CreatePDF(io.StringIO(html_content), dest=pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer

    except Exception as e:
        # Error fallback
        error_html = f"""
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        padding: 30px;
      }}
      h1 {{
        font-size: 36px;
        color: #003366;
        border-bottom: 5px solid #003366;
        padding-bottom: 10px;
        margin-bottom: 25px;
      }}
      p {{
        font-size: 18px;
        color: #333;
      }}
    </style>
  </head>
  <body>
    <h1>Error</h1>
    <p><strong>Detail:</strong> {e}</p>
  </body>
</html>
"""

        pdf_buffer = io.BytesIO()
        pisa.CreatePDF(io.StringIO(error_html), dest=pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer
