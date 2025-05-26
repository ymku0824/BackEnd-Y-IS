from models.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Sentence(db.Model):
    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(UUID(as_uuid=True), db.ForeignKey('videos.id', ondelete='CASCADE'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    group_number = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Sentence {self.number} - {self.start_time}>"
