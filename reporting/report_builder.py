import json
from datetime import datetime

class ReportBuilder:
    """
    Builds the final text and JSON reports from the collected data and analyses.
    """
    def __init__(self, village_data: dict, analysis_results: dict, growth_plan: str):
        self.village_data = village_data
        self.analysis_results = analysis_results
        self.growth_plan = growth_plan
        self.report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def build_text_report(self) -> str:
        """
        Generates a comprehensive, human-readable text report.
        """
        print(" -> Text report banaya ja raha hai... (Generating text report...)")
        
        village_name = self.village_data.get("village_name_and_state", "Unknown Village")
        
        # Helper to safely get analysis results
        def get_analysis(key, title):
            content = self.analysis_results.get(key, "No analysis available.")
            return f"--- {title} ---\n{content}\n\n"

        report = f"""
# Village Digital Twin Report: {village_name}
Report Generated on: {self.report_date}

==================================================
**1. Village Profile**
==================================================
{self.analysis_results.get('village_profile', 'No profile available.')}

==================================================
**2. Key Challenges & Opportunities**
==================================================

{get_analysis('problem_analysis', 'Problem Analysis')}
{get_analysis('shopkeeper_insights', 'Insights for Shopkeepers')}
{get_analysis('customer_recommendations', 'Recommendations for Villagers')}

==================================================
**3. Village Growth & Development Plan**
==================================================
{self.growth_plan}

--- End of Report ---
"""
        print("Text report taiyaar hai. (Text report is ready.)")
        return report.strip()

    def build_json_report(self) -> str:
        """
        Generates a JSON report containing all data.
        """
        print(" -> JSON report banaya ja raha hai... (Generating JSON report...)")
        
        report_data = {
            "report_metadata": {
                "report_title": f"Village Digital Twin Report: {self.village_data.get('village_name_and_state', 'Unknown Village')}",
                "generation_date": self.report_date,
            },
            "village_data": self.village_data,
            "analysis_and_recommendations": self.analysis_results,
            "growth_plan": self.growth_plan,
        }
        
        print("JSON report taiyaar hai. (JSON report is ready.)")
        return json.dumps(report_data, indent=4)

if __name__ == '__main__':
    # This is for testing the ReportBuilder directly.
    try:
        # Dummy data for testing
        dummy_village_data = {
            "village_name_and_state": "Basi, Uttar Pradesh",
            "population_approx": 5000,
            "main_occupation": "Agriculture"
        }
        
        dummy_analysis_results = {
            "village_profile": "Basi is a village in Uttar Pradesh...",
            "problem_analysis": "The main issues are contaminated drinking water...",
            "shopkeeper_insights": "Shopkeepers should stock more water purifiers...",
            "customer_recommendations": "Villagers could form a cooperative..."
        }
        
        dummy_growth_plan = """
**Phase 1: Short-Term (First 3 Months)**
*   Initiative: Water Quality Testing and Awareness Camp
    *   Responsible Stakeholder: Gram Panchayat & Health Workers
    *   Difficulty: Low
    *   Expected Impact: 4/5
"""

        print("--- Running ReportBuilder Test ---")
        builder = ReportBuilder(dummy_village_data, dummy_analysis_results, dummy_growth_plan)
        
        # Test text report
        text_report = builder.build_text_report()
        print("\n--- Generated Text Report ---")
        print(text_report)

        # Test JSON report
        json_report = builder.build_json_report()
        print("\n\n--- Generated JSON Report ---")
        print(json_report)

    except Exception as e:
        print(f"An error occurred in the test run: {e}")
