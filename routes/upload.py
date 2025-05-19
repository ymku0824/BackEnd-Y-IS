from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from services.db_service import save_metadata  # DB 저장 함수 임포트

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    category = request.form.get('category', 'default')
    user_id = request.form.get('user_id', 'anonymous')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 파일명에 UUID 추가하여 고유성 확보
    original_filename = file.filename
    extension = original_filename.rsplit('.', 1)[-1]
    video_id = str(uuid.uuid4())  # 고유한 디렉토리 이름
    safe_filename = f"{video_id}_{secure_filename(original_filename)}"
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], video_id)

    try:
        # 업로드 경로 생성
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, safe_filename)
        file.save(file_path)

        # ✅ DB에 메타데이터 저장
        metadata = {
            "video_id": video_id,
            "user_id": user_id,
            "category": category,
            "status": "uploaded",
            "file_url": file_path
        }
        save_metadata(video_id, metadata)

        return jsonify({
            'message': '비디오 업로드 성공',
            'video_id': video_id,
            'original_filename': original_filename,
            'file_path': file_path
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
