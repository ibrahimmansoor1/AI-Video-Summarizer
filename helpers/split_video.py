import ffmpeg
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

def split_video(input_path, chunk_duration=30):
    chunks = []
    output_dir = tempfile.mkdtemp()
    
    try:
        probe = ffmpeg.probe(input_path)
        duration = float(probe['streams'][0]['duration'])
        num_chunks = int(duration // chunk_duration) + (1 if duration % chunk_duration > 0 else 0)
        
        for i in range(num_chunks):
            start_time = i * chunk_duration
            output_path = os.path.join(output_dir, f"chunk_{i:03d}.mp4")
            
            (
                ffmpeg
                .input(input_path, ss=start_time, t=chunk_duration)
                .output(output_path, vcodec='copy', acodec='copy')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            if os.path.exists(output_path):
                chunks.append(output_path)
                
        return chunks, output_dir
        
    except Exception as e:
        logger.error(f"Error splitting video: {str(e)}")
        return [], output_dir