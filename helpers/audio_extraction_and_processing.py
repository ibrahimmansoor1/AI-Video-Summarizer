import ffmpeg
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

CHUNK_DURATION = 300  
MAX_AUDIO_SIZE = 25 * 1024 * 1024 

def extract_audio_from_video(video_path, output_path):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_path, acodec='mp3', ac=1, ar=16000)  
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return os.path.exists(output_path)
    except Exception as e:
        logger.error(f"Error extracting audio: {str(e)}")
        return False

def split_audio(input_path, chunk_duration=300):
    chunks = []
    output_dir = tempfile.mkdtemp()
    
    try:
        probe = ffmpeg.probe(input_path)
        duration = float(probe['streams'][0]['duration'])
        num_chunks = int(duration // chunk_duration) + (1 if duration % chunk_duration > 0 else 0)
        
        for i in range(num_chunks):
            start_time = i * chunk_duration
            output_path = os.path.join(output_dir, f"audio_chunk_{i:03d}.mp3")
            
            (
                ffmpeg
                .input(input_path, ss=start_time, t=chunk_duration)
                .output(output_path, acodec='mp3')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )

            if os.path.exists(output_path) and os.path.getsize(output_path) < MAX_AUDIO_SIZE:
                chunks.append(output_path)
            elif os.path.exists(output_path):
                logger.warning(f"Audio chunk {i} too large, skipping")
                
        return chunks, output_dir
        
    except Exception as e:
        logger.error(f"Error splitting audio: {str(e)}")
        return [], output_dir