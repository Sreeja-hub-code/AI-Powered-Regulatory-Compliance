# ai_service.py
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env file. Please add it.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Function to analyze text
def analyze_text_with_groq(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ Updated model name
            messages=[
                {"role": "system", "content": "You are a helpful AI compliance assistant."},
                {"role": "user", "content": text},
            ],
        )

        # Get the AI's reply
        ai_reply = response.choices[0].message.content
        return ai_reply

    except Exception as e:
        return f"❌ Error while analyzing text: {e}"