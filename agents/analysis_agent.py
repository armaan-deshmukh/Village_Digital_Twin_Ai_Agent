import json
from core.gemini_client import GeminiClient

class AnalysisAgent:
    """
    Performs various analyses based on the structured village data.
    This agent combines the logic for profiling, problem analysis, and
    generating insights for shopkeepers and customers.
    """
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    def analyze(self, village_data: dict) -> dict:
        """
        Runs all analyses and returns a dictionary with the results.

        Args:
            village_data: A dictionary containing the structured data about the village.

        Returns:
            A dictionary containing all the analysis reports.
        """
        print("\nAnalysis Agent: Shuru ho raha hai... (Starting analysis...)")
        
        village_profile = self._generate_village_profile(village_data)
        problem_analysis = self._analyze_problems(village_data)
        shopkeeper_insights = self._generate_shopkeeper_insights(village_data)
        customer_recommendations = self._generate_customer_recommendations(village_data)

        print("Analysis Agent: Sabhi analysis poore ho gaye. (All analyses completed.)")

        return {
            "village_profile": village_profile,
            "problem_analysis": problem_analysis,
            "shopkeeper_insights": shopkeeper_insights,
            "customer_recommendations": customer_recommendations,
        }

    def _generate_village_profile(self, village_data: dict) -> str:
        """Generates a narrative village profile."""
        print(" -> Village profile banaya ja raha hai... (Generating village profile...)")
        prompt = f"""
        Based on the following data, write a brief, engaging village profile in a narrative style. 
        The profile should be in simple, professional English, suitable for a report.
        It should cover key aspects like demographics, economy, and infrastructure.

        Village Data:
        {json.dumps(village_data, indent=2)}

        Generate the profile text.
        """
        return self.gemini_client.generate_text(prompt)

    def _analyze_problems(self, village_data: dict) -> str:
        """Analyzes the top 3 problems."""
        print(" -> Top 3 samasyaon ka vishleshan kiya ja raha hai... (Analyzing top 3 problems...)")
        # Ensure 'top_3_problems' key exists
        if "top_3_problems" not in village_data:
            return "No problems were listed in the initial data."
            
        prompt = f"""
        Based on the following village data, provide a detailed analysis of the top 3 problems mentioned.
        For each problem, include:
        1.  **Root Cause Analysis:** What are the likely underlying causes of this problem?
        2.  **Impact Assessment:** How does this problem affect the villagers' lives, economy, and well-being?
        3.  **Potential Solutions:** Suggest 2-3 practical and actionable solutions for each problem.

        Village Data:
        {json.dumps(village_data, indent=2)}

        Provide a detailed analysis for each of the top three problems.
        """
        return self.gemini_client.generate_text(prompt)

    def _generate_shopkeeper_insights(self, village_data: dict) -> str:
        """Generates insights for local shopkeepers."""
        print(" -> Dukandaron ke liye insights taiyaar ki ja rahi hain... (Generating insights for shopkeepers...)")
        prompt = f"""
        Act as a business consultant for shopkeepers in a small Indian village. Based on the provided data, generate actionable business insights.
        Include suggestions on:
        1.  **Top Product Categories:** What are the most needed products that are likely to sell well?
        2.  **Seasonal Demand:** Are there any products that would have higher demand during specific seasons?
        3.  **Inventory Management:** Tips on what to stock and how much, considering the village's economy.
        4.  **Customer Engagement:** How can they better serve their customers and build loyalty?

        Village Data:
        {json.dumps(village_data, indent=2)}

        Provide a concise report with these insights for the village shopkeepers.
        """
        return self.gemini_client.generate_text(prompt)

    def _generate_customer_recommendations(self, village_data: dict) -> str:
        """Generates recommendations for villagers."""
        print(" -> Grahakon ke liye sujhav taiyaar kiye ja rahe hain... (Generating recommendations for customers...)")
        prompt = f"""
        Act as a helpful assistant for the residents of an Indian village. Based on the village data, provide recommendations for products, services, or initiatives that could improve their daily lives.
        Consider the main occupations, problems, and available infrastructure.
        Suggest things that are practical, affordable, and accessible. For example, if internet is poor, don't suggest online services that require high bandwidth.

        Village Data:
        {json.dumps(village_data, indent=2)}

        Provide a list of 3-5 key recommendations for the villagers.
        """
        return self.gemini_client.generate_text(prompt)

if __name__ == '__main__':
    try:
       
        dummy_village_data = {
            "village_name_and_state": "Basi, Uttar Pradesh",
            "population_approx": 5000,
            "main_occupation": "Agriculture",
            "internet_availability": "3G/4G",
            "shops_schools_hospitals": "10 shops, 2 schools, 1 clinic",
            "top_3_problems": "1. Lack of clean drinking water, 2. Irregular electricity, 3. Poor road connectivity"
        }
        
        print("--- Running AnalysisAgent Test ---")
        gemini_client = GeminiClient()
        analysis_agent = AnalysisAgent(gemini_client)
        
        all_analyses = analysis_agent.analyze(dummy_village_data)
        
        print("\n\n--- Analysis Results ---")
        for key, value in all_analyses.items():
            print(f"\n--- {key.replace('_', ' ').title()} ---\n")
            print(value)
            
    except Exception as e:
        print(f"An error occurred in the test run: {e}")
