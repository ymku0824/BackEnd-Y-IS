import shutil
import subprocess
import os
from services.whisper_service import transcribe_audio
from services.db_service import save_metadata, save_sentences
from services.gemini_service import generate_chapter_titles
from services.grouping_service import apply_chapter_groups

def convert_mp4_to_mp3(mp4_path):
    mp3_path = mp4_path.replace(".mp4", ".mp3")
    try:
        subprocess.run(['ffmpeg', '-i', mp4_path, '-q:a', '0', '-map', 'a', mp3_path], check=True)
        print(f"[INFO] MP4 to MP3 conversion successful: {mp3_path}")
        return mp3_path
    except Exception as e:
        print(f"[ERROR] MP4 to MP3 conversion failed: {str(e)}")
        return None

def process_video(video_path, video_id, user_id, category):
    try:
        # Step 1: Convert MP4 to MP3
        audio_path = convert_mp4_to_mp3(video_path)
        if not audio_path:
            print("[ERROR] Audio conversion failed.")
            return None

        # Step 2: Transcribe audio
        transcription = transcribe_audio(audio_path)
        if not transcription:
            print("[ERROR] Transcription failed.")
            return None

        # Step 3: Save transcribed sentences to DB
        save_sentences(video_id, transcription)

        # Step 4: Generate chapter titles (can be improved later)
        chapter_path = generate_chapter_titles(audio_path, video_id)
        apply_chapter_groups(video_id, chapter_path)
        if not chapter_path:
            print("[ERROR] Chapter title generation failed.")
            return None

        # Step 5: Save metadata
        summary = "Generated summary"  # Placeholder
        metadata = {
            "video_id": video_id,
            "user_id": user_id,
            "category": category,
            "status": "processed",
            "file_url": video_path,
            "transcription": "\n".join([s["text"] for s in transcription]),
            "summary": summary
        }
        save_metadata(video_id, metadata)
        print("[INFO] Pipeline completed successfully.")
        return metadata
    except Exception as e:
        print(f"[ERROR] Pipeline processing failed: {str(e)}")
        return None
