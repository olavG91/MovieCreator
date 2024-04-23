import requests
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')

def create_audio(text):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/nPczCjzI2devNBz1zQrb"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": elevenlabs_api_key
    }

    data = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.7,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers)

    filename = f"temp/{uuid.uuid4()}.mp3"  # Generate a random filename
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    
    return filename