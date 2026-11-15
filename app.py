import streamlit as st
import requests
import pandas as pd
from database import init_db, save_results, load_history

# FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/analyze"

# Initialize your feedback.db table on startup
init_db()

st.set_page_config(page_title="Feedback Analyzer", page_icon="💬", layout="centered")
st.title("💬 Customer Feedback Analyzer")

# --- INPUT SECTION ---
review_text = st.text_area(
    "Enter a customer review:",
    placeholder="e.g., The delivery was super fast, but the food was cold.",
    height=100
)

if st.button("Analyze & Save", type="primary"):
    if not review_text.strip():
        st.warning("Please type a review first.")
    else:
        with st.spinner("Analyzing with Gemini..."):
            try:
                # 1. Call your FastAPI /analyze endpoint
                response = requests.post(API_URL, json={"text": review_text.strip()})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Ensure FastAPI returned valid analysis JSON and not an error string
                    if isinstance(data, dict) and "label" in data:
                        # 2. Format data as a list of dicts to match your save_results(results) function
                        record_to_save = [{
                            "review": review_text.strip(),
                            "label": data["label"],
                            "score": data["score"],
                            "theme": data["theme"]
                        }]
                        
                        # 3. Save to feedback.db using your function
                        save_results(record_to_save)
                        st.success("Saved to feedback.db!")
                        
                        # 4. Show result metrics on screen
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Label", data["label"].capitalize())
                        col2.metric("Score", f"{data['score']} / 5")
                        col3.metric("Theme", data["theme"])
                    else:
                        st.error(f"API Error: {data}")
                else:
                    st.error(f"Server returned status code {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI. Make sure Uvicorn is running on http://127.0.0.1:8000")

# --- HISTORY SECTION ---
st.divider()
st.subheader("📜 Saved History (from `feedback.db`)")

history_rows = load_history()

if history_rows:
    # Convert the SQLite rows from load_history() into a clean table
    df = pd.DataFrame(history_rows, columns=["Review", "Label", "Score", "Theme"])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No reviews in feedback.db yet. Analyze a review above to see it here!")