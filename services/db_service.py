from sqlalchemy.exc import SQLAlchemyError
from models import db, Video

def save_metadata(video_id, metadata):
    try:
        # Check for missing transcription and summary keys
        transcription = metadata.get("transcription", "N/A")
        summary = metadata.get("summary", "N/A")  # Add summary handling

        video = Video(
            video_id=video_id,
            user_id=metadata.get("user_id", "unknown"),
            category=metadata.get("category", "general"),
            status=metadata.get("status", "unknown"),
            file_url=metadata.get("file_url", "N/A"),
            transcription=transcription,
            summary=summary  # Save the summary to the database
        )
        db.session.add(video)
        db.session.commit()
        print(f"[INFO] Metadata saved for video ID: {video_id}")
    except SQLAlchemyError as e:
        print(f"[ERROR] Failed to save metadata: {str(e)}")  # Use specific SQLAlchemyError
    except Exception as e:
        print(f"[ERROR] Unexpected error while saving metadata: {str(e)}")

def get_metadata(video_id):
    """PostgreSQL에서 메타데이터 가져오기"""
    try:
        video = Video.query.filter_by(video_id=video_id).first()
        if video:
            return {
                "video_id": video.video_id,
                "user_id": video.user_id,
                "category": video.category,
                "status": video.status,
                "file_url": video.file_url,
                "transcription": video.transcription,
                "summary": video.summary  # Ensure summary is included
            }
        return None
    except SQLAlchemyError as e:
        print(f"[ERROR] 메타데이터 가져오기 실패: {e}")
        return None
