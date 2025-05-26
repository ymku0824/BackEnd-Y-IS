from models import db, Sentence
from datetime import timedelta

def save_sentences_from_whisper(segments, video_id):
    try:
        sentence_objects = []
        for idx, segment in enumerate(segments):
            # 초 단위 → HH:MM:SS 문자열로 변환
            start_time = str(timedelta(seconds=int(segment['start'])))
            sentence = Sentence(
                video_id=video_id,
                number=idx + 1,
                start_time=start_time,
                contents=segment['text'].strip(),
                group_number=0
            )
            sentence_objects.append(sentence)

        db.session.bulk_save_objects(sentence_objects)
        db.session.commit()
        print(f"[INFO] Saved {len(sentence_objects)} sentences for video {video_id}")
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed to save sentences: {str(e)}")
