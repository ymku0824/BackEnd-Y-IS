from app import app  # Flask 애플리케이션 가져오기
from models.db import db  # DB 객체 가져오기
from models.video import Video  # DB 모델 가져오기

# Flask 애플리케이션 컨텍스트에서 DB 초기화
with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        print("[INFO] 데이터베이스 초기화 완료")
    except Exception as e:
        print(f"[ERROR] 데이터베이스 초기화 실패: {e}")
