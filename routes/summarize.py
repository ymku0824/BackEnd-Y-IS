# routes/summarize.py
from flask import Blueprint, request, jsonify
from services.pipeline_service import process_video

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/summarize', methods=['POST'])
def summarize_video():
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        user_id = data.get('user_id', 'anonymous')
        category = data.get('category', 'general')
        video_path = f"static/uploads/{video_id}/original.mp4"
        
        # 카테고리 리스트 처리
        category_list = data.get('category', [])
        if not isinstance(category_list, list):
            category_list = [category_list]

        result = process_video(video_path, video_id, user_id, category_list)
        if not result:
            return jsonify({'error': 'Video processing failed'}), 500

        return jsonify({'message': 'Video processed successfully', 'video_id': video_id, 'metadata': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
