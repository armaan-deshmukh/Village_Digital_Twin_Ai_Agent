import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiClient:
    """
    A client to interact with the Google Gemini API.
    """
    def __init__(self, model_name="gemini-2.5-flash-lite"):
        """
        Initializes the Gemini client.
        - Loads environment variables from a .env file.
        - Configures the Gemini API with the provided API key.
        - Initializes the specified generative model.
        """
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file or environment variables.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        print("Gemini Client initialized successfully.")

    def generate_text(self, prompt: str) -> str:
        """
        Generates text using the configured Gemini model.

        Args:
            prompt: The text prompt to send to the model.

        Returns:
            The generated text as a string.
        
        Raises:
            Exception: If the text generation fails.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"An error occurred during text generation: {e}")
            return f"Error: Could not generate response from Gemini. Details: {e}"

if __name__ == '__main__':
    try:
        # testing purposes. It requires a .env file with a valid API key.
        client = GeminiClient()
        
        # Create a dummy .env file for testing if it doesn't exist
        if not os.path.exists('.env'):
            with open('.env', 'w') as f:
                f.write('GEMINI_API_KEY="YOUR_API_KEY_HERE"\n')
            print("Created a dummy .env file. Please replace YOUR_API_KEY_HERE with your actual key.")
            # Exit because the key is a dummy
            exit()

        print("Sending a test prompt to Gemini...")
        test_prompt = "Hello, what is the capital of India?"
        response_text = client.generate_text(test_prompt)
        
        print(f"\nPrompt: {test_prompt}")
        print(f"Response: {response_text}")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
