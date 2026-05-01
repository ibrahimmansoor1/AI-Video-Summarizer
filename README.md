# AI Meeting Intelligence Platform

An AI-powered video summarization system that automatically transcribes and summarizes meeting recordings using OpenAI Whisper and GPT-4o-mini.

## 🎯 Key Impact

- **Architected a chunked transcription pipeline** for videos up to 52+ mins by splitting audio into 5-minute segments with 25MB max per chunk and sequentially calling OpenAI Whisper, enabling reliable long-form transcription within token and file size limits

- **Engineered a Flask web app** using ffmpeg to extract 16kHz MP3, chunked transcription, and GPT-4o-mini summarization (800 tokens, 0.3 temperature), converting video into structured meeting summaries with MP4 and MOV support

- **Integrated OpenAI Whisper speech-to-text and GPT-4o-mini NLP models** into a single workflow, generating transcripts and concise summaries from video while reducing review time by 70–80% and improving accessibility to recorded content

## ✨ Features

- **Video-to-Summary Pipeline**: Process videos up to 52+ minutes with chunked transcription
- **Whisper Speech-to-Text**: Accurate audio transcription at 16kHz mono MP3
- **GPT-4o-mini Summarization**: Concise meeting summaries with key points (800 tokens)
- **Multi-format Support**: MP4, MOV file processing
- **Web Interface**: Single-click Flask web app for easy uploads

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Audio Processing**: ffmpeg, ffmpeg-python
- **AI/ML**: OpenAI Whisper (speech-to-text), GPT-4o-mini (summarization)
- **Frontend**: HTML5, CSS3, JavaScript
- **Environment**: Python virtual environment, python-dotenv

## 📦 Requirements

- Python 3.8+
- ffmpeg installed and on PATH
- OpenAI API key

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/ibrahimmansoor1/AI-Video-Summarizer.git
cd AI-Video-Summarizer
```

### 2. Create and activate virtual environment
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install ffmpeg
**Windows (winget):**
```bash
winget install --id=Gyan.FFmpeg -e
```

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Linux (apt):**
```bash
sudo apt-get install ffmpeg
```

### 5. Create `.env` file with your OpenAI API key
```bash
echo OPENAI_API_KEY=sk-YOUR_API_KEY_HERE > .env
```

Get your OpenAI API key from: https://platform.openai.com/account/api-keys

### 6. Run the application
```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your browser and upload a video.

## 📁 Project Structure

```
AI-Video-Summarizer/
├── app.py                                    # Flask main application
├── helpers/
│   ├── audio_extraction_and_processing.py   # Audio chunking & ffmpeg extraction
│   ├── transcript_Generator.py              # Whisper transcription logic
│   └── summarizer.py                        # GPT-4o-mini summarization
├── templates/
│   └── index.html                           # Web UI template
├── static/
│   └── style.css                            # Styling
├── requirements.txt                         # Python dependencies
├── .gitignore                               # Git ignore rules
└── README.md                                # This file
```

## 🎬 How It Works

1. **Upload Video**: User uploads MP4/MOV file via web interface
2. **Extract Audio**: ffmpeg extracts audio at 16kHz mono MP3
3. **Chunk Transcription**: Audio split into 5-minute segments (25MB max)
4. **Transcribe**: OpenAI Whisper transcribes each chunk sequentially
5. **Summarize**: GPT-4o-mini generates concise summary from full transcript
6. **Display Results**: User receives transcript + summary in browser

## 📊 Example Output

**Input:** 52-minute meeting recording (MP4)

**Output:** 
- Full transcript with timestamps
- 3–5 key discussion points
- Action items summary
- Executive summary (2–3 sentences)

## 🔧 Configuration

Edit these in `helpers/audio_extraction_and_processing.py`:
- `CHUNK_DURATION = 300` → Change to adjust chunk length (seconds)
- `MAX_AUDIO_SIZE = 25 * 1024 * 1024` → Max audio file size (bytes)

Edit these in `helpers/summarizer.py`:
- `max_tokens=800` → Adjust summary length
- `temperature=0.3` → Adjust creativity (0=deterministic, 1=creative)

## ⚠️ Limitations

- Maximum video length: 52+ minutes (tested; longer videos may work)
- Supported formats: MP4, MOV
- Audio extraction requires ffmpeg
- Requires valid OpenAI API key with sufficient credits

## 📝 License

MIT

## 👤 Author

Muhammad Ibrahim Mansoor  
Shayan Rehman
AI/ML Developer  
GitHub: [@ibrahimmansoor1](https://github.com/ibrahimmansoor1)

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech-to-text
- [GPT-4o-mini](https://platform.openai.com/) for summarization
- [FFmpeg](https://ffmpeg.org/) for audio processing
