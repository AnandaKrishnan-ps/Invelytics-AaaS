def get_analytics_prompt(today: str, inventory_summary: str) -> str:
    return f"""
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


def get_recommendations_prompt(today: str, inventory_summary: str) -> str:
    return f"""
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


def get_combined_prompt(analytics_response: str, recommendation_response: str) -> str:
    return f"""
# ROLE:
    - You are an expert business analyst AI that generates HTML reports.

# OBJECTIVE:
    - Create a well-formatted HTML report that combines the analytics and recommendations.
    - Use semantic HTML tags: <section>, <h2>, <p>, <ul>, <li>, etc.
    - Organize into two main sections: "Inventory Analysis" and "Strategic Recommendations".
    - Keep the HTML minimal and clean, suitable for embedding in a webpage.

# CONTENT TO FORMAT:

## INVENTORY ANALYSIS:
{analytics_response}

## STRATEGIC RECOMMENDATIONS:
{recommendation_response}
"""
