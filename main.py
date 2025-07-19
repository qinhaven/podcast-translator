from app.transcription import transcribe_audio
from app.translation import translate_text_to_chinese
from app.tts import synthesize_speech

if __name__ == "__main__":
    input_file = "huberman_sleep.mp3"

    #1. Transcribe
    transcript = transcribe_audio(input_file, model_size="small")
    print("\n--- Transcript Preview ---\n")
    print(transcript[:1000])

    #2. Translate
    print("\n--- Translating to Chinese ---\n")
    chinese_text = translate_text_to_chinese(transcript)
    print("\n--- Translated Text ---\n")
    print(chinese_text[:1000])

    # #3. Save Chinese output
    # with open("huberman_sleep_transcript_zh.txt", "w", encoding="utf-8") as f:
    #     f.write(chinese_text)
    # print("Saved to 'huberman_sleep_transcript_zh.txt'")

    # english_txt = "huberman_sleep_transcript.txt"
    # chinese_txt = "huberman_sleep_transcript_zh.txt"
    # # translate_file(english_txt, chinese_txt)

    #3. Synthesize
    print("\n--- Synthesizing Speech ---\n")
    synthesize_speech(chinese_text[:250], voice="4VZIsMPtgggwNg7OXbPY", output_path="huberman_sleep_zh.wav")
    print("\n--- Speech Synthesis Complete ---\n")