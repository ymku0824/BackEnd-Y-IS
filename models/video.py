from models.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = db.Column(db.String(100), unique=True, nullable=False)  # 영상 식별자
    user_id = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="uploaded")
    file_url = db.Column(db.String(300), nullable=False)
    transcription = db.Column(db.Text, nullable=True)
    summary = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Video {self.video_id}>"
