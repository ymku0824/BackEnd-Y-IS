# services/grouping_service.py
import pandas as pd
from models import db
from models.sentence import Sentence
from datetime import timedelta

def parse_time(time_str):
    """시간 문자열을 timedelta 객체로 변환 ('HH:MM:SS' 또는 'MM:SS')"""
    try:
        parts = time_str.strip().split(':')
        parts = [int(p) for p in parts]
        if len(parts) == 3:
            return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
        elif len(parts) == 2:
            return timedelta(minutes=parts[0], seconds=parts[1])
        else:
            return timedelta(seconds=int(parts[0]))
    except:
        return timedelta(seconds=0)

def apply_chapter_groups(video_id, chapter_csv_path):
    try:
        # 1. 챕터 타임스탬프 읽기
        chapter_df = pd.read_csv(chapter_csv_path)
        chapter_df["timestamp"] = chapter_df["timestamp"].apply(parse_time)
        chapter_df = chapter_df.sort_values("timestamp").reset_index(drop=True)

        # 2. 해당 비디오의 문장 가져오기
        sentences = Sentence.query.filter_by(video_id=video_id).order_by(Sentence.number).all()
        if not sentences:
            print("[WARN] No sentences found for video.")
            return False

        # 3. 문장을 챕터 타임스탬프 기준으로 그룹화
        group_idx = 0
        current_chapter_time = chapter_df.iloc[group_idx]["timestamp"] if not chapter_df.empty else None

        for sentence in sentences:
            sentence_time = parse_time(sentence.start_time)

            # 다음 챕터 기준 시간 도달하면 group index 증가
            while group_idx + 1 < len(chapter_df) and sentence_time >= chapter_df.iloc[group_idx + 1]["timestamp"]:
                group_idx += 1

            sentence.group_number = group_idx

        # 4. 저장
        db.session.commit()
        print(f"[INFO] Group numbers updated for video {video_id}")
        return True

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed to apply chapter groups: {str(e)}")
        return False
