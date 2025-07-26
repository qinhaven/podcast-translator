import whisper
import os
from pathlib import Path

def transcribe_audio(file_path: str, model_size: str = "small") -> str:
    """
    Transcribe an audio file into English text using Whisper.
    
    Args:
        file_path (str): Path to the input audio file (.mp3, .wav, etc.)
        model_size (str): Whisper model to use ("tiny", "base", "small", etc.)

    Returns:
        str: Transcribed English text
        
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        ImportError: If Whisper is not installed
        Exception: For other transcription errors
    """
    
    # Check if whisper is available
    try:
        import whisper
    except ImportError:
        raise ImportError("Whisper is not installed. Please install it with: pip install openai-whisper")

    # Validate input file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        print(f"Loading Whisper model ({model_size})...")
        model = whisper.load_model(model_size)

        print(f"Transcribing: {file_path}")
        result = model.transcribe(file_path)

        text = result["text"]

        # Save transcript to a text file, optional
        input_path = Path(file_path)
        transcript_path = input_path.with_suffix("").with_name(input_path.stem + "_transcript.txt")
        
        try:
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Transcription saved to: {transcript_path}")
        except IOError as e:
            print(f"Warning: Could not save transcript file: {e}")
        
        return text
        
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")