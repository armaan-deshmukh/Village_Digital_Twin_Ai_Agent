# Village Digital Twin AI Agent

This project is a command-line based AI agent that creates a "digital twin" of an Indian village. Using the Gemini 2.5 Flash Lite model, it gathers information about a village through a conversational interface, performs a detailed analysis, and generates a comprehensive development plan.

The agent is designed with a modular, multi-agent architecture to handle different aspects of the process, from data collection to report generation.

## Features

- Conversational Data Gathering: Interactively collects village data in a natural way (Hinglish).
- Intelligent Clarification: Asks follow-up questions to ensure data completeness and accuracy.
- Comprehensive Analysis:
    - Village Profile: Creates a narrative profile of the village.
    - Problem Analysis: Identifies root causes, impacts, and solutions for key problems.
    - Business Intelligence: Provides actionable insights for local shopkeepers.
    - Citizen Recommendations: Suggests practical improvements for villagers.
- Strategic Growth Planning: Generates a phased (3, 6, 12-month) growth plan with stakeholders, difficulty levels, and impact scores.
- Multi-Format Reporting: Delivers the final report in multiple formats:
    - Clean, readable text in the console.
    - Structured JSON file.
    - Formatted PDF document.
- Session Memory: (Implicit) The agent processes all information within a single run, creating a cohesive report at the end.

## Architecture

The application follows a logical multi-agent design pattern, where different modules are responsible for specific tasks:

- `main.py`: The central orchestrator that manages the application flow.
- `core/gemini_client.py`: A client to handle all communications with the Google Gemini API.
- `agents/`: A package containing the logic for different "agents":
    - `input_agent.py`: Manages the user interaction for data gathering.
    - `analysis_agent.py`: Performs all the analyses (profiling, problems, business, and customer insights).
    - `planning_agent.py`: Creates the future-state growth plan.
- `reporting/`: A package for generating the final outputs:
    - `report_builder.py`: Assembles the text and JSON reports.
    - `pdf_generator.py`: Creates the PDF report using the FPDF2 library.

## Setup and Installation

Follow these steps to set up and run the project on your local Windows machine.

1. Prerequisites:
   - Python 3.8 or higher.
   - Git for cloning the repository.

2. Clone the Repository:
   ...bash
   git clone <repository_url>
   cd village_digital_twin
   ...
   *(Replace `<repository_url>` with the actual URL of your Git repository)*

3. Create a Virtual Environment:
   It's highly recommended to use a virtual environment to manage project dependencies.
   ...bash
   python -m venv venv
   .\venv\Scripts\activate
   ...

4. Install Dependencies:
   Install all the required libraries using the `requirements.txt` file.
   ...bash
   pip install -r requirements.txt
   ...
   *Note: For PDF generation, the `fpdf2` library uses fonts. The included `pdf_generator.py` attempts to use the DejaVu font. If not available on your system, it will fall back to Arial, which may affect the rendering of some characters.*

5. Set Up Your API Key:
   The agent needs a Google Gemini API key to function.
   a. Create a `.env` file in the project root directory by copying the example file:
      ...bash
      copy .env.example .env
      ...
   b. Open the new `.env` file in a text editor.
   c. Replace `"YOUR_API_KEY_HERE"` with your actual Gemini API key. You can obtain a key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## How to Run

Once the setup is complete, you can start the agent by running the `main.py` script:
...bash
python main.py
...

The agent will then start the conversation, asking you for information about the village.

## Example Interaction

...
$ python main.py
--- Village Digital Twin AI Agent Initializing ---
Gemini Client initialized successfully.
Namaste! Main Village Digital Twin AI Agent hoon.
Mujhe aapke gaon ka digital twin banane ke liye kuch jaankari chahiye.

Q: Gaon ka naam kya hai aur ye kaunse state me hai? (What is the name of the village and in which state is it?)
A: My village is Basi in Uttar Pradesh.
Q: Yahan ki anumanit जनसंख्या (approx. population) kitni hai? (What is the approximate population?)
A: Around 5000 people.
...
(The conversation continues until all initial data is gathered)
...
Report taiyaar hai. Kya aap ise anya format me chahte hain? (JSON/PDF/No): pdf
...
After this, a PDF report will be saved in the `reports` directory within the project folder.
