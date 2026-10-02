import os

from flask import Flask
from backend.admin import admin_bp
from backend.auth import auth_bp, oauth
from backend.routes import main_bp
from backend.pdf_export import pdf_bp
from backend.report import report_bp
from backend.interview import interview_bp
from backend.mock_interview import mock_interview_bp

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

oauth.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(main_bp)
app.register_blueprint(pdf_bp)
app.register_blueprint(report_bp)
app.register_blueprint(interview_bp)
app.register_blueprint(mock_interview_bp)

if __name__ == "__main__":
    app.run(debug=True)
