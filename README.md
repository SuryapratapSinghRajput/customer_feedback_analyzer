***Customer Feedback Analyzer***
An AI-powered web application that analyzes customer reviews in real time. Built with FastAPI, Streamlit, SQLite, and the Google Gemini API, this project extracts sentiment labels, numerical ratings, and primary themes from customer feedback and stores the results in a local database.

***Features***
AI Sentiment & Theme Extraction: Uses Google's gemini-3.8-flash model with structured JSON outputs (response_schema) to classify reviews into:

Label: positive, negative, or neutral

Score: 1 (very bad) to 5 (very good)

Theme: A single lowercase keyword summarizing the main topic (e.g., delivery, taste, price, service, quality)

RESTful Backend: Powered by FastAPI and Pydantic for clean request validation and fast API responses.

Interactive UI: Built with Streamlit for easy review submission, instant metric visualization, and history browsing.

Persistent Storage: Automatically saves every analyzed review into a local SQLite database (feedback.db) and displays past entries in a clean data table.




***Project Structure***
project_feedback_analyzer/
├── app.py              # Streamlit frontend application
├── main.py             # FastAPI backend & Gemini API integration
├── database.py         # SQLite database initialization, saving, and loading logic
├── feedback.db         # Local SQLite database (auto-generated on first run)
├── pyproject.toml      # Project dependencies and configuration
├── uv.lock             # Dependency lockfile (for uv package manager)
├── .env                # Environment variables (API keys)
├── .python-version     # Python version specification (3.14.7)
└── README.md           # Project documentation


***Tech Stack***
Frontend: Streamlit, Pandas, Requests
Backend: FastAPI, Uvicorn, Pydantic
AI Model: Google GenAI SDK (gemini-3.8-flash)
Database: SQLite3
Environment Management: uv / python-dotenv


***Getting Started***
Prerequisites
Python 3.14+ (or as specified in .python-version)
A Google Gemini API Key (get one from Google AI Studio)
uv (recommended) or pip


1. Clone the Repository
git clone "https://github.com/SuryapratapSinghRajput/customer_feedback_analyzer.git"


2. Install Dependencies
Using uv:
       uv sync
Or using standard pip:
     python -m venv .venv
     .venv\Scripts\activate
     pip install fastapi uvicorn pydantic python-dotenv google-genai streamlit requests pandas


3. Configure Environment Variables
Create a .env file in the root directory and add your Gemini API key:
GEMINI_API_KEY= enter api key

***Running the Application***
Because this project separates the backend API from the frontend interface, you will need to run two terminal processes simultaneously.

Terminal 1: Start the FastAPI Backend
uvicorn main:app --reload

The API will be available at
 http://127.0.0.1:8000 (interactive docs at http://127.0.0.1:8000/docs).

Terminal 2: Start the Streamlit Frontend
         streamlit run app.py

The web interface will open automatically in your browser at http://localhost:8501.

***API Reference***

POST /analyze:
Analyzes a customer review string and returns structured feedback metrics.
Request Body:
{
  "text": "The delivery was super fast, but the food was cold."
}
Response (200 OK):
{
  "label": "neutral",
  "score": 3,
  "theme": "delivery"
}


***Database Schema***

The SQLite database (feedback.db) contains a single table named feedback:

column    Type                   Description
id        INTEGER PRIMARY KEY    Auto-incrementing unique identifier
review    TEXT                   Original customer review text
label     TEXT                   Sentiment (positive, negative, neutral)
score     INTEGER                Rating from 1 to 5
theme     TEXT                   One-word lowercase topic summary