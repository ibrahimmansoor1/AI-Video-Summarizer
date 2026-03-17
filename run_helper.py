from helpers.audio_extraction_and_processing import extract_audio_from_video, split_audio, CHUNK_DURATION
import os, traceback
inp = r"test_videos\sintel_trailer_720p.mp4"
out = r"test_videos\from_helper.mp3"
print("Calling helper...", inp, "->", out)
try:
    ok = extract_audio_from_video(inp, out)
    print("extract_audio_from_video returned:", ok)
    if ok and os.path.exists(out):
        print("Output size (bytes):", os.path.getsize(out))
        chunks, outdir = split_audio(out, CHUNK_DURATION)
        print("split_audio returned", len(chunks), "chunks; outdir:", outdir)
    else:
        print("Output file missing or extraction failed.")
except Exception:
    traceback.print_exc()
    raise
