from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# \ud658\uacbd \ubcc0\uc218 \ub85c\ub4dc
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # \ubaa8\ub4e0 \ucd9c\ucc98 \ud5c8\uc6a9

# \uc11c\ubc84 \uc124\uc815
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv("MAX_CONTENT_LENGTH"))

# DB \uc124\uc815
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB \ucd08\uae30\ud654
from models.db import db  # DB \uc778\uc2a4\ud134\uc2a4 \uac00\uc838\uc624\uae30
db.init_app(app)

@app.route('/')
def index():
    return "PostgreSQL \uc5f0\ub3d9 \ud14c\uc2a4\ud2b8 \ud398\uc774\uc9c0"

# \ube14\ub8e8\ud504\ub9b0\ud2b8 \ub4f1\ub85d\uc744 \ub9e8 \uc544\ub798\ub85c \uc774\ub3d9\ud558\uc5ec \uc21c\ud658\ucc38\uc870 \ubc29\uc9c0
from routes.upload import upload_bp
from routes.summarize import summarize_bp
from routes.edit import edit_bp
from routes.status import status_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(upload_bp)
app.register_blueprint(summarize_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(status_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5555,debug=True)
