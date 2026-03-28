import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elevenlabs.client import ElevenLabs

app = FastAPI()

# This allows your WordPress site to talk to this Render server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# These pull the keys you saved in Render's "Environment Variables"
API_KEY = os.getenv("ELEVEN_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

client = ElevenLabs(api_key=API_KEY)

@app.get("/")
def home():
    return {"message": "AI Backend is Live"}

@app.get("/get-signed-url")
def get_signed_url():
    try:
        # This is the line that was causing the error - fixed now!
        response = client.conversational_ai.get_signed_url_for_agent(agent_id=AGENT_ID)
        return {"url": response}
    except Exception as e:
        return {"error": str(e)}
