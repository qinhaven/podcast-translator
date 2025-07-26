import os
from elevenlabs import generate, save, set_api_key
from dotenv import load_dotenv

load_dotenv()

def synthesize_speech(text: str, voice: str = "4VZIsMPtgggwNg7OXbPY", output_path: str = "output.wav", model: str = "eleven_multilingual_v2") -> str:
    """
    Generates spoken Mandarin audio from text using ElevenLabs API.

    Args:
        text (str): The Mandarin text to convert to speech.
        voice (str): Voice name or ID from ElevenLabs (e.g., "4VZIsMPtgggwNg7OXbPY").
        output_path (str): Path to save the generated audio file (.wav).
        model (str): ElevenLabs model to use for speech generation.

    Returns:
        str: Path to the generated audio file
        
    Raises:
        ValueError: If text is empty or invalid
        RuntimeError: If API key is missing
        Exception: For other API or file errors
    """
    
    # Validate input
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    if not output_path:
        raise ValueError("Output path cannot be empty")
    
    # Check API key
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not found in environment variables")
    
    try:
        # Set API key
        set_api_key(api_key)
        
        # Generate audio
        audio = generate(
            text=text,
            voice=voice,
            model=model
        )
        
        # Save audio
        save(audio, output_path)
        print(f"Audio saved to {output_path}")
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Speech synthesis failed: {str(e)}")