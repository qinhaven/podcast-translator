import os
from elevenlabs import generate, save, set_api_key
from dotenv import load_dotenv

load_dotenv()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

def synthesize_speech(text: str, voice: str = "4VZIsMPtgggwNg7OXbPY", output_path: str = "output.wav"):
    """
    Generates spoken Mandarin audio from text using ElevenLabs API.

    Args:
        text (str): The Mandarin text to convert to speech.
        voice (str): Voice name or ID from ElevenLabs (e.g., "4VZIsMPtgggwNg7OXbPY").
        output_path (str): Path to save the generated audio file (.wav).
    """
    try:
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_multilingual_v2"
        )
        save(audio, output_path)
        print(f"Audio saved to {output_path}")
    except Exception as e:
        print(f"Error generating audio: {e}")