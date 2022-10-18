from flask import Flask
from api.short_answer_assessment_api import answer_assessment_bp

app = Flask(__name__)

app.register_blueprint(answer_assessment_bp)

app.config.from_pyfile('config.py')