from dotenv import load_dotenv
import os
from groq import Groq

# 1️⃣ Load environment variables from .env file
load_dotenv()

# 2️⃣ Read the API key
api_key = os.getenv("GROQ_API_KEY")

# 3️⃣ Check if the key loaded correctly
if not api_key:
    print("❌ GROQ_API_KEY not found. Please check your .env file.")
else:
    print("🔑 API key loaded successfully.")

# 4️⃣ Initialize the Groq client
try:
    client = Groq(api_key=api_key)

    # 5️⃣ Simple test message for AI analysis
    rag_chunk1 = "Hello, this is a test for the AI compliance checker."

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an AI compliance assistant."},
            {"role": "user", "content": rag_chunk1},
        ],
    )

    print("AI Analysis Result:")
    print(chat_completion.choices[0].message.content)

except Exception as e:
    print("❌ Error while analyzing text:", e)
