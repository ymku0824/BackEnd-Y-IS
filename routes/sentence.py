from flask import Blueprint, jsonify, request
from models.sentence import Sentence
from models import db
from collections import defaultdict
from sqlalchemy import asc

sentence_bp = Blueprint("sentence", __name__)

@sentence_bp.route("/sentences/summary/<video_id>", methods=["GET"])
def get_sentence_summary_json(video_id):
    try:
        # 전체 문장 불러오기
        sentences = Sentence.query.filter_by(video_id=video_id).order_by(
            Sentence.group_number, Sentence.number
        ).all()

        # 그룹 단위로 묶기
        grouped = defaultdict(list)
        meta = {}

        for sentence in sentences:
            g = sentence.group_number
            grouped[g].append(sentence.contents)
            if g not in meta:
                meta[g] = {
                    "timestamp": sentence.start_time,
                    "chapter_title": sentence.chapter_title or "제목 없음"
                }

        # 결과 정리
        result = []
        for g in sorted(grouped.keys()):
            result.append({
                "id": g,
                "timestamp": meta[g]["timestamp"],
                "chapter_title": meta[g]["chapter_title"],
                "sentences": grouped[g]
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
