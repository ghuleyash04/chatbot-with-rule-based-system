from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

# Explicitly load .env file from current directory
load_dotenv(dotenv_path=".env")
# Get API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Please set it in your .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)

class chatRequest(BaseModel):
    message: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

def get_bot_response(user_message: str) -> str:
    message = user_message.lower()
    

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": message}
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )

    return chat_completion.choices[0].message.content

@app.post("/chat")
async def chat(request: chatRequest):
    reply = get_bot_response(request.message)
    return {"reply": reply}