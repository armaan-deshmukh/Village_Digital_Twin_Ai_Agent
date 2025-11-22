import os
from core.gemini_client import GeminiClient
from agents.input_agent import InputAgent
from agents.analysis_agent import AnalysisAgent
from agents.planning_agent import PlanningAgent
from reporting.report_builder import ReportBuilder
from reporting.pdf_generator import PDFGenerator

def main():
    """
    The main function to run the Village Digital Twin AI Agent.
    """
    try:
        # 1. Initialization
        print("--- Village Digital Twin AI Agent Initializing ---")
        gemini_client = GeminiClient()
        
        # Initialize Agents
        input_agent = InputAgent(gemini_client)
        analysis_agent = AnalysisAgent(gemini_client)
        planning_agent = PlanningAgent(gemini_client)
        
        # --- Main Workflow ---
        
        # 2. Data Gathering
        village_data = input_agent.gather_data()
        if not village_data:
            print("Could not gather village data. Exiting.")
            return

        # 3. Analysis
        analysis_results = analysis_agent.analyze(village_data)

        # 4. Planning
        growth_plan = planning_agent.create_growth_plan(village_data, analysis_results)

        # 5. Report Generation
        print("\n--- Final Report Generation ---")
        builder = ReportBuilder(village_data, analysis_results, growth_plan)
        
        # Generate and print the main text report
        text_report = builder.build_text_report()
        print("\n" + "="*50)
        print("         VILLAGE DIGITAL TWIN - FINAL REPORT")
        print("="*50)
        print(text_report)
        print("="*50)

        # --- Optional Formats ---
        
        while True:
            choice = input("\nReport taiyaar hai. Kya aap ise anya format me chahte hain? (JSON/PDF/No): ").lower()
            
            if choice == 'json':
                json_report = builder.build_json_report()
                village_name = village_data.get("village_name_and_state", "UnknownVillage")
                safe_village_name = "".join(x for x in village_name if x.isalnum() or x in " _-").strip()
                filename = f"reports/Report_{safe_village_name}.json"
                
                if not os.path.exists('reports'):
                    os.makedirs('reports')
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(json_report)
                
                final_path = os.path.abspath(filename)
                print(f"JSON report safaltapoorvak save ho gaya hai: {final_path}")

            elif choice == 'pdf':
                pdf_generator = PDFGenerator()
                village_name = village_data.get("village_name_and_state", "UnknownVillage")
                pdf_path = pdf_generator.generate_pdf(text_report, village_name)
                print(f"PDF generation status: {pdf_path}")

            elif choice in ['no', 'n', 'exit', 'quit']:
                print("Dhanyavaad! (Thank you!)")
                break
            else:
                print("Aमान्य vikalp. Kripya 'JSON', 'PDF', ya 'No' me se chunein. (Invalid option. Please choose 'JSON', 'PDF', or 'No'.)")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("The program will now exit.")

if __name__ == '__main__':
    main()
