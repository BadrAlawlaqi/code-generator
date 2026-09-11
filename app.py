import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# 1. Page Configuration
st.set_page_config(
    page_title="Code Snippet Generator",
    page_icon="💻",
    layout="centered"
)

# 2. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 3. User Interface (English)
st.title("💻 Code Snippet Generator")
st.write("Generate high-quality code snippets in various programming languages from natural language descriptions.")

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox(
        "Select Programming Language:",
        ["Python", "JavaScript", "TypeScript", "HTML/CSS", "C++", "Java", "SQL", "Go", "Rust", "PHP"]
    )

# Prompt Input
prompt_input = st.text_area(
    "Code Description:",
    placeholder="e.g., A Python function that filters even numbers from a list and returns them sorted.",
    height=150
)

# 4. Code Generation Logic
if st.button("🚀 Generate Code", type="primary"):
    if not api_key:
        st.error("❌ Gemini API key not found. Please ensure it is set in your `.env` file.")
    elif not prompt_input.strip():
        st.warning("⚠️ Please provide a description for the code.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Generating code... Please wait."):
                prompt = (
                    f"You are an expert software engineer. Generate clean, efficient, and well-commented "
                    f"code snippets in {language} based on this description: {prompt_input}. "
                    f"Provide only the code snippet in markdown code block syntax with a brief explanation if necessary."
                )
                
                # Updated working model name
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                )
                
                st.success("Code generated successfully!")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")