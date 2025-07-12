from app.transcription import transcribe_audio

if __name__ == "__main__":
    input_file = "huberman_sleep.mp3"
    transcript = transcribe_audio(input_file, model_size="small")
    print("\n--- Transcript Preview ---\n")
    print(transcript[:1000])