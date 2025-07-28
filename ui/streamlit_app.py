import sys
import os
import tempfile

# Add root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.search import search_podcast, download_episode_mp3
from app.transcription import transcribe_audio
from app.translation import translate_text_to_chinese
from app.tts import synthesize_speech

st.set_page_config(page_title="Podcast Translator", layout="centered")

st.title("Podcast Translator")
st.markdown("🎧 Search for an English podcast and get a Mandarin translation as audio!")

# --- STEP 1: Search and Select Episode ---
query = st.text_input("🔍 Search for a podcast episode")

if query:
    with st.spinner("Searching..."):
        results = search_podcast(query)

    if results:
        options = {f"{r['title_original']} – {r['podcast_title_original']}": r for r in results}
        choice_label = st.selectbox("Select an episode", list(options.keys()))
        selected = options[choice_label]

        st.audio(selected['audio'], format='audio/mp3')
        
        if st.button("Translate this episode"):
            try:
                # --- STEP 2: Download MP3 ---
                with st.spinner("Downloading episode..."):
                    file_path = download_episode_mp3(selected["audio"])
                
                # --- STEP 3: Transcribe ---
                with st.spinner("Transcribing..."):
                    transcript = transcribe_audio(file_path, model_size="small")
                    st.success("✅ Transcription complete")
                    st.text_area("Transcription Preview", transcript[:500] + "...", height=150)

                # --- STEP 4: Translate ---
                with st.spinner("Translating..."):
                    chinese_text = translate_text_to_chinese(transcript)
                    st.success("✅ Translation complete")
                    st.text_area("Translation Preview", chinese_text[:500] + "...", height=150)

                # --- STEP 5: Text-to-Speech ---
                with st.spinner("Synthesizing..."):
                    base_name = selected["title_original"].replace(" ", "_").replace("/", "_")[:50]
                    output_audio_path = f"{base_name}_zh.wav"
                    chinese_transcript_path = f"{base_name}_zh.txt"

                    with open(chinese_transcript_path, "w", encoding="utf-8") as f:
                        f.write(chinese_text)

                    synthesize_speech(chinese_text, output_path=output_audio_path)

                    st.audio(output_audio_path, format="audio/wav")
                    with open(output_audio_path, "rb") as f:
                        st.download_button("⬇️ Download Translated Audio", f, file_name=output_audio_path)

                    with open(chinese_transcript_path, "rb") as f:
                        st.download_button("⬇️ Download Chinese Transcript", f, file_name=chinese_transcript_path)

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
            finally:
                try:
                    os.remove(file_path)
                except:
                    pass
    else:
        st.warning("No results found. Try a different search.")
else:
    st.info("Type a podcast topic or episode name to begin.")  