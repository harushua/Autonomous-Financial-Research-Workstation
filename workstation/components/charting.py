import matplotlib.pyplot as plt
import os
import json

def create_and_save_charts(chart_data: list, quantitative_data: dict, output_dir: str = "outputs"):
    """
    Generates and saves charts based on the provided data.

    Args:
        chart_data: A list of dictionaries with chart titles and data queries.
        quantitative_data: The raw quantitative data from Polygon.
        output_dir: The directory to save the chart images.

    Returns:
        A list of file paths to the generated chart images.
    """
    print("--- Running Chart Generation Node ---")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chart_paths = []
    
    # For this example, we'll create a simple revenue bar chart if the data is available.
    for chart_info in chart_data:
        if "revenue" in chart_info.get("title", "").lower():
            try:
                # FIX: The financial data from the tool is a JSON string. We must parse it first.
                financials_str = quantitative_data.get("financials", "[]")
                financials_list = json.loads(financials_str)
                
                revenues = []
                periods = []
                for report in financials_list:
                    if report.get("timeframe") == "quarterly":
                        income_statement = report.get("financials", {}).get("income_statement", {})
                        revenue = income_statement.get("revenues", {}).get("value")
                        period = f"{report.get('fiscal_year')}-{report.get('fiscal_period')}"
                        if revenue and period:
                            revenues.append(revenue / 1_000_000_000) # Convert to billions
                            periods.append(period)
                
                if not revenues:
                    print("   ⚠️ No quarterly revenue data found to create chart.")
                    continue

                # Create the bar chart
                plt.figure(figsize=(10, 6))
                # Sort data chronologically before plotting
                sorted_data = sorted(zip(periods, revenues))
                sorted_periods, sorted_revenues = zip(*sorted_data)

                plt.bar(sorted_periods, sorted_revenues, color='skyblue')
                plt.xlabel("Fiscal Period")
                plt.ylabel("Revenue (in Billions USD)")
                plt.title("Quarterly Revenue")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()

                # Save the chart
                chart_path = os.path.join(output_dir, "quarterly_revenue.png")
                plt.savefig(chart_path)
                plt.close()
                chart_paths.append(chart_path)
                print(f"   ✅ Chart saved to: {chart_path}")

            except Exception as e:
                print(f"   ❌ Error creating revenue chart: {e}")

    return chart_paths
