from fpdf import FPDF
import os

class PDFGenerator:
    """
    Generates a PDF report from a text string.
    """
    def generate_pdf(self, text_report: str, village_name: str) -> str:
        """
        Creates a PDF file from the text report content.

        Args:
            text_report: The string content of the report.
            village_name: The name of the village, used for the filename.

        Returns:
            The path to the saved PDF file.
        """
        print(" -> PDF report banaya ja raha hai... (Generating PDF report...)")
        
        pdf = FPDF()
        pdf.add_page()

        try:
            pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
            pdf.set_font('DejaVu', '', 10)
        except Exception:
            print(" -> Warning: DejaVu font not found. Falling back to Arial. Special characters might not render correctly.")
            pdf.set_font('Arial', '', 10)
        
        # Report Title
        pdf.set_font_size(16)
        pdf.cell(0, 10, f"Village Digital Twin Report: {village_name}", ln=True, align='C')
        pdf.ln(10)

        sanitized_report = text_report.encode('latin-1', 'replace').decode('latin-1')

        # Report Body
        pdf.set_font_size(10)
        # Use multi_cell to handle newlines and long text
        pdf.multi_cell(0, 5, sanitized_report)

        # Create a 'reports' directory if it doesn't exist
        if not os.path.exists('reports'):
            os.makedirs('reports')

        # Generate a clean filename
        safe_village_name = "".join(x for x in village_name if x.isalnum() or x in " _-").strip()
        filename = f"reports/Report_{safe_village_name}.pdf"
        
        try:
            pdf.output(filename)
            final_path = os.path.abspath(filename)
            print(f"PDF report safaltapoorvak save ho gaya hai: {final_path} (PDF report saved successfully at the path)")
            return final_path
        except Exception as e:
            error_message = f"PDF report save nahi ho saka. (Could not save PDF report.) Error: {e}"
            print(error_message)
            return error_message


if __name__ == '__main__':
    # This is for testing the PDFGenerator directly.
    dummy_text_report = """
# Village Digital Twin Report: Basi

Report Generated on: 2025-11-22 13:30:00

==================================================
**1. Village Profile**
==================================================
Basi is a village in Uttar Pradesh...

==================================================
**2. Key Challenges & Opportunities**
==================================================

--- Problem Analysis ---
The main issues are contaminated drinking water...

--- Insights for Shopkeepers ---
Shopkeepers should stock more water purifiers...

--- Recommendations for Villagers ---
Villagers could form a cooperative...

==================================================
**3. Village Growth & Development Plan**
==================================================

**Phase 1: Short-Term (First 3 Months)**
*   Initiative: Water Quality Testing and Awareness Camp
    *   Responsible Stakeholder: Gram Panchayat & Health Workers
    *   Difficulty: Low
    *   Expected Impact: 4/5

--- End of Report ---
    """
    
    print("--- Running PDFGenerator Test ---")
    pdf_gen = PDFGenerator()
    pdf_path = pdf_gen.generate_pdf(dummy_text_report, "Basi_Test")
    
    if "Error" not in pdf_path:
        print(f"\nTest PDF created at: {pdf_path}")
        print("Please open the file to verify its contents.")

