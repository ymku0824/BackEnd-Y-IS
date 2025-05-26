from flask import Blueprint, request, jsonify
from models.sentence import Sentence
from models import db
from sqlalchemy.exc import SQLAlchemyError

sentence_bp = Blueprint('sentence', __name__)

@sentence_bp.route('/sentences/group-update', methods=['PATCH'])
def update_sentence_groups():
    try:
        data = request.get_json()
        video_id = data.get("video_id")
        updates = data.get("updates", [])

        if not video_id or not updates:
            return jsonify({"error": "Missing video_id or updates"}), 400

        # 각 업데이트 항목 처리
        for item in updates:
            number = item.get("number")
            group_number = item.get("group_number")
            if number is None or group_number is None:
                continue

            sentence = Sentence.query.filter_by(video_id=video_id, number=number).first()
            if sentence:
                sentence.group_number = group_number

        db.session.commit()
        return jsonify({"message": "Group numbers updated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
