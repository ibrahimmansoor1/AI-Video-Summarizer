from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv
import logging
import tempfile
import shutil
from openai import OpenAI
from pathlib import Path
from helpers.audio_extraction_and_processing import extract_audio_from_video, split_audio, CHUNK_DURATION
# from helpers.split_video import split_video
from helpers.transcript_Generator import transcribe_audio_with_whisper
from helpers.summarizer import generate_summary_with_gpt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    logger.info("Upload endpoint called")
    
    if "file" not in request.files:
        logger.error("No file part in request")
        return jsonify({"error": "No file part"}), 400
        
    file = request.files["file"]
    if file.filename == "":
        logger.error("No file selected")
        return jsonify({"error": "No selected file"}), 400

    # logger.info(f"Processing file: {file.filename}")
    
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in video_extensions:
        return render_template("index.html", 
                             summary="Error: Please upload a video file",
                             transcript="")
    
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
    file.save(temp_input.name)
    temp_input.close()
    
    try:
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_audio.close()
        
        # logger.info("Extracting audio from video...")
        if not extract_audio_from_video(temp_input.name, temp_audio.name):
            return render_template("index.html", 
                                 summary="Error: Could not extract audio from video",
                                 transcript="")

        #logger.info("Splitting audio into chunks...")
        audio_chunks, audio_output_dir = split_audio(temp_audio.name, CHUNK_DURATION)
        
        if not audio_chunks:
            return render_template("index.html", 
                                 summary="Error: Could not split audio",
                                 transcript="")

        transcripts = []
        logger.info(f"Transcribing {len(audio_chunks)} audio chunks...")
        
        for i, chunk_path in enumerate(audio_chunks):
            logger.info(f"Transcribing chunk {i+1}/{len(audio_chunks)}")
            
            transcript = transcribe_audio_with_whisper(chunk_path, client)
            if transcript and not str(transcript).startswith("Error"):
                start_time = i * CHUNK_DURATION
                end_time = (i + 1) * CHUNK_DURATION
                transcripts.append(f"[{start_time//60:02d}:{start_time%60:02d} - {end_time//60:02d}:{end_time%60:02d}] {transcript}")
            else:
                transcripts.append(f"[Chunk {i+1}] {transcript}")

        full_transcript = "\n\n".join(transcripts)
        logger.info("Generating summary from transcript...")
        summary = generate_summary_with_gpt(full_transcript, client)
        
        return render_template("index.html", 
                             summary=summary,
                             transcript=full_transcript)
        
    except Exception as e:
        # logger.error(f"Unexpected error: {str(e)}")
        return render_template("index.html", 
                             summary=f"Unexpected error: {str(e)}",
                             transcript="")
        
    finally:
        try:
            os.unlink(temp_input.name)
            if 'temp_audio' in locals():
                os.unlink(temp_audio.name)
            if 'audio_output_dir' in locals():
                shutil.rmtree(audio_output_dir)
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)