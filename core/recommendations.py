import io
from datetime import datetime
from typing import List

from core.inventory_logic import get_all_inventory_items
from db.database import Database
from models.inventory_schema import InventoryResponse
from ollama import AsyncClient
from xhtml2pdf import pisa

OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"


def compress_inventory(inventory: List[InventoryResponse]) -> str:
    """Compress inventory into a token-efficient summary."""
    return '- ' + "\n- ".join(
        [
            f"{item.item_id}: {item.name}, Qty={item.quantity}, ${item.price}, "
            f"{item.category or 'N/A'}, {item.last_updated.strftime('%Y-%m-%d')}"
            for item in inventory
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


async def generate_html_report(inventory: List[InventoryResponse]) -> str:
    """Pipeline to create the complete HTML report."""
    today = datetime.now().strftime("%Y-%m-%d")
    inventory_summary = compress_inventory(inventory)
    print(inventory_summary)

    # Prompt 1: Analytics
    analytics_prompt = f"""
# ROLE:
    -   You are a business analyst AI. 
    
# INSTRUCTIONS:
    -   Analyze the following inventory data as of {today}.
    -   Give a detailed report on 
        -   stock status, 
        -   fast/slow moving items, 
        -   over/under-stocked items,
        -   general insights.

# CURRENT INVENTORY:
{inventory_summary}
"""


    # Prompt 2: Recommendations
    recommendation_prompt = f"""
# ROLE:
    -   You are a strategic business advisor AI.

# INSTRUCTIONS:
    -   Based on the inventory data as of {today}, provide actionable business recommendations.
    -   Focus your suggestions on:
        -   marketing improvements,
        -   stock management strategies,
        -   cost reduction opportunities.
    -   Keep the recommendations clear and implementable.

# CURRENT INVENTORY:
{inventory_summary}
    """

    analytics_response = await call_ollama(
    analytics_prompt, system="You write professional business analytics reports."
    )

    # Call Ollama API for recommendations
    recommendation_response = await call_ollama(
        recommendation_prompt,
        system="You are a strategic advisor that outputs business suggestions.",
    )

    # Combine responses
    return f"""
    <html>
        <head><title>Daily Inventory Report - {today}</title></head>
        <body>
            <h1>Daily Inventory Report</h1>
            <h2>Date: {today}</h2>
            <hr/>
            {analytics_response}
            <hr/>
            {recommendation_response}
        </body>
    </html>
    """


async def generate_daily_recommendations_pdf() -> io.BytesIO:
    """Master function to create final PDF."""
    try:
        inventory = await get_all_inventory_items(
            Database._db.inventory, ignore_limit=True
        )
        inventory.sort(key=lambda item: item.last_updated, reverse=True)
        inventory = inventory[:50]

        html_content = await generate_html_report(inventory)

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
