import json
from core.gemini_client import GeminiClient

class InputAgent:
    """
    Handles gathering and structuring initial village data from the user.
    """
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
        self.initial_questions = [
            "Gaon ka naam kya hai aur ye kaunse state me hai? (What is the name of the village and in which state is it?)",
            "Yahan ki anumanit जनसंख्या (approx. population) kitni hai? (What is the approximate population?)",
            "Logon ka mukhya kaam kya hai (kheti, majduri, chota business, etc.)? (What is the main occupation of the people - farming, labor, small business, etc?)",
            "Internet ki suvidha kaisi hai (nahi hai, 2G, 3G/4G, ya high-speed)? (What is the internet availability - none, 2G, 3G/4G, 5G, or high-speed?)",
            "Anumanit kitni dukanein, schools, aur hospitals/clinics hain? (Approximately how many shops, schools, and hospitals/clinics are there?)",
            "Aapke anusaar gaon ki sabse badi samasyayein kya hain? (According to you, what are the biggest problems in the village?)"
        ]
        self.village_data = {}

    def gather_data(self) -> dict:
        """
        Gathers village data from the user, asking initial and follow-up questions.
        """
        print("Namaste! Main Village Digital Twin AI Agent hoon.")
        print("Mujhe aapke gaon ka digital twin banane ke liye kuch jaankari chahiye.\n")

        # Ask initial questions
        initial_answers = {}
        for question in self.initial_questions:
            answer = input(f"Q: {question}\nA: ")
            initial_answers[question] = answer
        
        # Use LLM to check for completeness and ask follow-up questions
        return self._clarify_and_structure(initial_answers)

    def _clarify_and_structure(self, answers: dict) -> dict:
        """
        Uses Gemini to check for incomplete answers, ask for clarification,
        and structure the data.
        """
        print("\nDhanyavaad! Main di gayi jaankari ko process kar raha hoon...")

        # Create a prompt for the LLM
        prompt = f"""
        Here is the initial information gathered about an Indian village. Your task is to act as a data validation and structuring assistant.
        
        1.  **Analyze the answers:** Review the provided answers for completeness and clarity.
        2.  **Identify Gaps:** If any answer is vague, incomplete, or seems ambiguous, formulate a clear, simple follow-up question in Hinglish (Hindi in Roman script) to get the missing information. Only ask for what is missing.
        3.  **Structure the Data:** Once all necessary information is present, structure the data into a clean JSON object. If you have to ask follow-up questions, wait until you have the answers before creating the final JSON.

        **Initial Data:**
        {json.dumps(answers, indent=2)}

        **Your Response Format:**

        *   **If clarification is needed:** Respond with ONLY the follow-up questions, one per line. Do not add any other text before or after the questions.
        *   **If no clarification is needed:** Respond with ONLY the final JSON object, enclosed in ```json ... ```.

        Let's begin. Analyze the provided data and proceed.
        """

        current_answers = answers.copy()
        
        while True:
            response = self.gemini_client.generate_text(prompt)
            response = response.strip()

            if response.startswith("```json"):
                # Data is structured, break the loop
                try:
                    json_str = response.split('```json\n')[1].split('\n```')[0]
                    self.village_data = json.loads(json_str)
                    print("Jaankari safaltapoorvak structure ho gayi hai.")
                    return self.village_data
                except (json.JSONDecodeError, IndexError) as e:
                    print(f"Error parsing JSON from model response: {e}")
                    print("Retrying clarification...")
                    # Add the problematic response to the prompt for context
                    prompt += f"\nI previously received this problematic response: {response}. Please try again to produce a valid JSON or ask clarifying questions."
                    continue # Retry
            else:
                # Follow-up questions were returned
                follow_up_questions = response.split('\n')
                print("\nKuch aur jaankari chahiye:\n")
                for question in follow_up_questions:
                    if question.strip():
                        answer = input(f"Q: {question.strip()}\nA: ")
                        current_answers[question.strip()] = answer
                
                # Re-prompt with the updated answers
                prompt = f"""
                Thank you for the additional information. Here is the updated data. Please review it again. If it's complete, structure it as a JSON object. Otherwise, ask more follow-up questions.

                **Updated Data:**
                {json.dumps(current_answers, indent=2)}

                **Your Response Format:**

                *   **If clarification is needed:** Respond with ONLY the follow-up questions, one per line.
                *   **If no clarification is needed:** Respond with ONLY the final JSON object, enclosed in ```json ... ```.
                """
        
if __name__ == '__main__':
    # testing the InputAgent directly.
    try:
        gemini_client = GeminiClient()
        input_agent = InputAgent(gemini_client)
        final_data = input_agent.gather_data()
        print("\n--- Final Structured Data ---")
        print(json.dumps(final_data, indent=4))
    except Exception as e:
        print(f"An error occurred in the test run: {e}")
