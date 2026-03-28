import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from elevenlabs.client import ElevenLabs

# 1. Initialize the App
app = FastAPI()

# 2. Security: Allow your WordPress site to talk to this Backend
# Replace "*" with "https://yourdomain.com" later for extra security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Get your Secrets from Render's Environment Variables
# (We don't hardcode them here so they stay safe)
API_KEY = os.getenv("ELEVEN_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

# 4. Initialize the ElevenLabs Client
client = ElevenLabs(api_key=API_KEY)

@app.get("/")
def home():
    return {"message": "The AI Backend is Running!"}

@app.get("/get-signed-url")
def get_signed_url():
    """
    This endpoint is called by your WordPress site.
    It asks ElevenLabs for a temporary 'Signed URL' (Guest Pass).
    """
    if not API_KEY or not AGENT_ID:
        raise HTTPException(status_code=500, detail="Server configuration missing keys.")

    try:
        # Request the temporary URL from ElevenLabs
        signed_url = client.conversational_ai.get_signed_url(agent_id=AGENT_ID)
        return {"url": signed_url}
    except Exception as e:
        print(f"Error fetching signed URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Note: Render uses the 'Start Command' we set earlier to run this file.