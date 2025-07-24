import streamlit as st
import os
from app.transcription import transcribe_audio
from app.translation import translate_text_to_chinese
from app.tts import synthesize_speech

st.set_page_config(page_title="Podcast Translator", layout="centered")

st.title("Podcast Translator")
st.markdown("Upload an English podcast, and get a Mandarin translation as audio!")

uploaded_file = st.file_uploader("Upload your podcast (.mp3)", type=["mp3"])
if uploaded_file:
    filename = uploaded_file.name
    file_path = os.path.join(".", filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded: {filename}")

if st.button("Translate"):
    with st.spinner("Transcribing..."):
        transcript = transcribe_audio(file_path, model_size="small")
        chinese_txt_path = filename.replace(".mp3", "_zh.txt")
        with open(chinese_txt_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        st.success("Transcription complete")

    with st.spinner("Translating..."):
        chinese_text = translate_text_to_chinese(transcript)
        st.success("Translation complete")

    with st.spinner("Synthesizing..."):
        output_audio_path = filename.replace(".mp3", "_zh.wav")
        synthesize_speech(chinese_text, output_path=output_audio_path)
        st.audio(output_audio_path, format="audio/wav")
        with open(output_audio_path, "rb") as f:
            st.download_button("Download Translated Podcast", f, file_name=output_audio_path)

    #os.remove(file_path)