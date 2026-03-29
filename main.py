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

@app.get("/get-signed-url")
def get_signed_url():
    # .strip() removes any accidental hidden spaces or line breaks
    api_key = os.getenv("ELEVEN_API_KEY", "").strip()
    agent_id = os.getenv("AGENT_ID", "").strip()

    # If your Agent ID in Render starts with 'agent_', try removing it 
    # and just using the random letters/numbers.
    clean_agent_id = agent_id.replace("agent_", "")

    url = f"https://api.elevenlabs.io/v1/convai/conversation/get_signed_url?agent_id={clean_agent_id}"
    
    headers = {
        "xi-api-key": api_key  # This must be EXACTLY this lowercase/hyphenated name
    }

    try:
        print(f"Attempting to reach ElevenLabs for Agent: {clean_agent_id}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 401:
            return {"error": "Unauthorized. Please check if your API Key has 'Conversational AI' permissions enabled in ElevenLabs settings."}
        
        response.raise_for_status()
        data = response.json()
        return {"url": data["signed_url"]}
        
    except Exception as e:
        return {"error": str(e)}
