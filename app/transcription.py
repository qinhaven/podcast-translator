import whisper
import os

def transcribe_audio(file_path: str, model_size: "small") -> str:
    """
    Transcribe an audio file into English text using Whisper.
    
    Args:
        file_path (str): Path to the input audio file (.mp3, .wav, etc.)
        model_size (str): Whisper model to use ("tiny", "base", "small", etc.)

    Returns:
        str: Transcribed English text
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Loading Whisper model ({model_size})...")
    model = whisper.load_model(model_size)

    print(f"Transcribing: {file_path}")
    result = model.transcribe(file_path)

    text = result["text"]

    # Save transcript to a text file, optional
    transcript_path = file_path.replace(".mp3", "_transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Transcription saved to: {transcript_path}")
    return text