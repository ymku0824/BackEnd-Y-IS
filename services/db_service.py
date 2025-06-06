from sqlalchemy.exc import SQLAlchemyError
from models import db, Video
from models.sentence import Sentence

def save_sentences(video_id, sentences):
    try:
        sentence_objects = []
        for idx, item in enumerate(sentences):
            sentence = Sentence(
                video_id=video_id,
                number=idx + 1,
                start_time=item['timestamp'],
                contents=item['text'],
                group_number=0  # 초기 그룹 번호
            )
            sentence_objects.append(sentence)

        db.session.bulk_save_objects(sentence_objects)
        db.session.commit()
        print(f"[INFO] Saved {len(sentences)} sentences for video {video_id}")
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed to save sentences: {str(e)}")


def save_metadata(video_id, metadata):
    try:
        transcription = metadata.get("transcription", "N/A")
        summary = metadata.get("summary", "N/A")

        video = Video(
            id=video_id,  # ✅ 반드시 필요!
            video_id=str(video_id),
            user_id=metadata.get("user_id", "unknown"),
            category=metadata.get("category", "general"),
            status=metadata.get("status", "unknown"),
            file_url=metadata.get("file_url", "N/A"),
            transcription=transcription,
            summary=summary
        )
        db.session.add(video)
        db.session.commit()
        print(f"[INFO] Metadata saved for video ID: {video_id}")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"[ERROR] Failed to save metadata: {str(e)}")
    except Exception as e:
        db.session.rollback()
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
                "summary": video.summary
            }
        return None
    except SQLAlchemyError as e:
        print(f"[ERROR] 메타데이터 가져오기 실패: {e}")
        return None
