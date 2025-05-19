# dashboard.py - Displays the list of processed videos and their status
from flask import Blueprint, jsonify
from models.db import db  # 수정: app 대신 db 모듈에서 직접 가져오기

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    try:
        videos = []
        # DB에서 모든 비디오 메타데이터 조회
        results = db.session.execute("SELECT * FROM videos").fetchall()
        for row in results:
            videos.append({
                'video_id': row.video_id,
                'user_id': row.user_id,
                'category': row.category,
                'status': row.status,
                'file_url': row.file_url
            })
        return jsonify({'videos': videos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
