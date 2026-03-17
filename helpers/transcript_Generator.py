from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

def transcribe_audio_with_whisper(audio_path, client):
    try:
        with open(audio_path, 'rb') as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return response
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return f"Error transcribing: {str(e)}"