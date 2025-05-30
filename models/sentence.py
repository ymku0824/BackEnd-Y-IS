from models.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Sentence(db.Model):
    __tablename__ = 'sentences'
    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #videos_id: videos 테이블과 연동하기 위한 FK
    video_id = db.Column(UUID(as_uuid=True), db.ForeignKey('videos.id', ondelete='CASCADE'), nullable=False)
    #number: 문장 순서별로 부여하는 숫자
    number = db.Column(db.Integer, nullable=False)
    #시작 스탬프(실제 결과물로 반환해야 하는 타임스탬프)
    start_time = db.Column(db.String(20), nullable=False)
    #contents: 문장(whisper에서 뽑아와서 저장)
    contents = db.Column(db.Text, nullable=False)
    #group_number: 그룹 번호(나중에 이거 업데이트해서 수정 사항 반영합니다)
    group_number = db.Column(db.Integer, nullable=False, default=0)
    #chapter_title: 챕터 제목
    chapter_title = db.Column(db.String(255), nullable=True)
    def __repr__(self):
        return f"<Sentence {self.number} - {self.start_time}>"

