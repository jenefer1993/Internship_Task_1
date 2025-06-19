from dotenv import load_dotenv
import os
import textwrap
import google.generativeai as genai
import streamlit as st
from collections import Counter
import re

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize model and chat
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# ---------- Streamlit App ---------- #
st.set_page_config(page_title="GEMINI CHATBOT")
st.title("🤖 GEMINI CHATBOT with ANALYTICS")

# Initialize session state
if 'queries' not in st.session_state:
    st.session_state.queries = []
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = []
if 'keywords' not in st.session_state:
    st.session_state.keywords = []

# Input field
user_input = st.text_input("Type your question:")
submit = st.button("Submit")

# If submitted, get response and store interaction
if submit and user_input:
    response = get_gemini_response(user_input)
    full_response = ""
    st.subheader("🤖 Gemini Response")
    for chunk in response:
        st.write(chunk.text)
        full_response += chunk.text
    
    # Save to session state
    st.session_state.queries.append(user_input)
    st.session_state.responses.append(full_response)

    # Extract simple keywords (you can replace with advanced NLP later)
    words = re.findall(r'\b\w+\b', user_input.lower())
    st.session_state.keywords.extend(words)

    # Satisfaction rating
    rating = st.slider("How satisfied are you with this response?", 1, 5, 3)
    st.session_state.ratings.append(rating)

# ---------- Dashboard ---------- #
with st.sidebar:
    st.header("📊 Chatbot Analytics")

    st.write(f"🔢 Total Queries: {len(st.session_state.queries)}")
    
    if st.session_state.queries:
        avg_rating = sum(st.session_state.ratings) / len(st.session_state.ratings)
        st.write(f"⭐️ Average Satisfaction: {avg_rating:.2f} / 5")
        
        # Top Keywords
        keyword_counts = Counter(st.session_state.keywords)
        common_keywords = keyword_counts.most_common(5)
        st.write("🔥 Frequent Topics:")
        for word, count in common_keywords:
            st.write(f"- {word} ({count})")
