from sqlalchemy.dialects.postgresql import UUID
import uuid
from models.db import db

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    transcription = db.Column(db.Text)
    summary = db.Column(db.Text)
