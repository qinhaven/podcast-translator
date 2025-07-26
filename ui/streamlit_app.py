import sys
import os
import tempfile

# Add root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.transcription import transcribe_audio
from app.translation import translate_text_to_chinese
from app.tts import synthesize_speech

st.set_page_config(page_title="Podcast Translator", layout="centered")

st.title("Podcast Translator")
st.markdown("Upload an English podcast, and get a Mandarin translation as audio!")

# Accept more audio formats
uploaded_file = st.file_uploader("Upload your podcast", type=["mp3", "wav", "m4a", "flac", "ogg"])

if uploaded_file:
    # Create a temporary file with proper path handling
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        file_path = tmp_file.name
    
    st.success(f"Uploaded: {uploaded_file.name}")
    
    # Only show translate button after file is uploaded
    if st.button("Translate"):
        try:
            with st.spinner("Transcribing..."):
                transcript = transcribe_audio(file_path, model_size="small") # small is the best for speed + accuracy
                st.success("Transcription complete")
                st.text_area("Transcription Preview", transcript[:500] + "...", height=150)

            with st.spinner("Translating..."):
                chinese_text = translate_text_to_chinese(transcript)
                st.success("Translation complete")
                st.text_area("Translation Preview", chinese_text[:500] + "...", height=150)

            with st.spinner("Synthesizing..."):
                # Create output filenames based on original filename
                base_name = uploaded_file.name.rsplit('.', 1)[0]  # Remove extension properly
                output_audio_path = f"{base_name}_zh.wav"
                chinese_transcript_path = f"{base_name}_zh.txt"
                
                # Save Chinese transcript to file
                with open(chinese_transcript_path, "w", encoding="utf-8") as f:
                    f.write(chinese_text)
                st.success(f"Chinese transcript saved to: {chinese_transcript_path}")
                
                synthesize_speech(chinese_text, output_path=output_audio_path)
                
                # Display audio and download buttons
                st.audio(output_audio_path, format="audio/wav")
                with open(output_audio_path, "rb") as f:
                    st.download_button("Download Translated Audio", f, file_name=output_audio_path)
                
                # Download Chinese transcript
                with open(chinese_transcript_path, "rb") as f:
                    st.download_button("Download Chinese Transcript", f, file_name=chinese_transcript_path)
                    
        except FileNotFoundError as e:
            st.error(f"File error: {str(e)}")
        except ImportError as e:
            st.error(f"Missing dependency: {str(e)}")
        except Exception as e:
            st.error(f"Transcription failed: {str(e)}")
        finally:
            # Clean up temporary file
            try:
                os.unlink(file_path)
            except:
                pass
else:
    st.info("Please upload an audio file to begin translation.")