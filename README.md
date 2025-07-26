
# 🎧 Podcast Translator

A comprehensive tool that transcribes English podcasts, translates them to Mandarin Chinese using OpenAI GPT, and generates natural Mandarin speech using ElevenLabs TTS.

Built with modern AI technologies — Whisper for transcription, OpenAI for translation, and ElevenLabs for speech synthesis.

---

## 🚀 Features

- 🎵 **Multi-format Audio Support**: Upload MP3, WAV, M4A, FLAC, or OGG files
- 📝 **High-Quality Transcription**: Powered by OpenAI Whisper with multiple model sizes
- 🌐 **AI-Powered Translation**: Fluent Mandarin translation using OpenAI GPT models
- 🔊 **Natural Speech Synthesis**: Mandarin audio generation with ElevenLabs
- 🖥️ **User-Friendly Interface**: Clean Streamlit web app with real-time progress
- 💾 **File Management**: Automatic saving of transcripts and audio files
- 🛡️ **Robust Error Handling**: Comprehensive error handling and user feedback

---

## 🏗️ Project Structure

```
podcast_translator/
├── app/
│   ├── transcription.py    # Whisper-based audio transcription
│   ├── translation.py      # OpenAI GPT translation to Mandarin
│   └── tts.py             # ElevenLabs speech synthesis
├── ui/
│   └── streamlit_app.py   # Streamlit web interface
├── main.py                # Command-line interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🧰 Tech Stack

- **Python 3.8+**
- **[OpenAI Whisper](https://github.com/openai/whisper)** - Audio transcription
- **[OpenAI API](https://platform.openai.com/)** - Text translation (GPT-4o-mini)
- **[ElevenLabs TTS](https://www.elevenlabs.io/)** - Speech synthesis
- **[Streamlit](https://streamlit.io/)** - Web interface
- **FFmpeg** - Audio processing backend

---

## 📦 Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/qinhaven/podcast-translator.git
cd podcast-translator
```

### 2. **Install Dependencies**
```bash
# Using pip
pip install -r requirements.txt

# Or using conda (recommended)
conda create -n podcast-translator python=3.10
conda activate podcast-translator
pip install -r requirements.txt
```

### 3. **Set Up API Keys**
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 4. **Install FFmpeg** (Required for audio processing)
- **Windows**: Download from [FFmpeg](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

---

## ▶️ Usage

### **Web Interface (Recommended)**
```bash
streamlit run ui/streamlit_app.py
```

**Steps:**
1. Upload an audio file (MP3, WAV, M4A, FLAC, or OGG)
2. Click "Translate" to start processing
3. View transcription and translation previews
4. Download the Mandarin audio and transcript files

### **Command Line Interface**
```bash
python main.py
```

---

## 📋 Dependencies

```
streamlit          # Web interface
openai             # OpenAI API for translation
openai-whisper     # Audio transcription
torch              # PyTorch (required by Whisper)
elevenlabs         # Text-to-speech API
pydub              # Audio processing
python-dotenv      # Environment variable management
requests           # HTTP requests
tqdm               # Progress bars
```

---

## 🔧 Configuration

### **Whisper Model Sizes**
- `tiny` - Fastest, least accurate
- `base` - Small, fast
- `small` - Good balance (default)
- `medium` - Better accuracy
- `large` - Best accuracy, slowest

### **OpenAI Models**
- `gpt-4o-mini` - Fast, cost-effective (default)
- `gpt-4o` - Higher quality, more expensive

---

## 🐛 Troubleshooting

### **Common Issues**
1. **"API key not found"** - Check your `.env` file
2. **"FFmpeg not found"** - Install FFmpeg and add to PATH
3. **"Transcription failed"** - Check audio file format and size
4. **"Translation failed"** - Verify OpenAI API key and quota

### **Audio File Requirements**
- Supported formats: MP3, WAV, M4A, FLAC, OGG
- Recommended size: Under 50MB for faster processing
- Audio quality: Clear speech for better transcription

---

## 🚀 Future Enhancements

- 🌍 Multi-language translation support
- 🔊 Better audio stitching
- 🧱 Unit tests
- ☁️ Online deployment via Streamlit Cloud

---

## 📄 License

MIT License
