import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("ELEVEN_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

@app.get("/")
def home():
    return {"message": "AI Backend is Live"}

@app.get("/get-signed-url")
def get_signed_url():
    try:
        # We call the ElevenLabs API directly - no more "attribute" errors!
        url = f"https://api.elevenlabs.io/v1/convai/conversation/get_signed_url?agent_id={AGENT_ID}"
        headers = {"xi-api-key": API_KEY}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return {"url": data["signed_url"]}
    except Exception as e:
        return {"error": str(e)}
