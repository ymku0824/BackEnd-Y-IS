from flask import Blueprint, jsonify
from models.video import Video
from sqlalchemy.exc import DataError
import uuid

status_bp = Blueprint('status', __name__)

@status_bp.route('/status/<video_id>', methods=['GET'])
def get_video_status(video_id):
    try:
        # Convert video_id to UUID
        try:
            uuid_obj = uuid.UUID(video_id)
        except ValueError:
            return jsonify({'error': 'Invalid video ID format'}), 400

        # Fetch video by video_id field (not by primary key 'id')
        video = Video.query.filter_by(video_id=str(uuid_obj)).first()
        if not video:
            return jsonify({'error': 'Video not found'}), 404

        return jsonify({
            'video_id': video.video_id,
            'status': video.status,
            'metadata': {
                'user_id': video.user_id,
                'category': video.category,
                'summary': video.summary,
                'file_url': video.file_url
            }
        }), 200
    except DataError:
        return jsonify({'error': 'Invalid video ID format in database'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
