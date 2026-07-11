from flask import Flask
from backend.auth import auth_bp
from backend.routes import main_bp
from backend.pdf_export import pdf_bp
from backend.report import report_bp
from backend.interview import interview_bp

app = Flask(__name__)

app.secret_key = "ai_interview_secret_key"

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)


@app.route("/")
def home():
    return {"status": "success", "message": "AI Interview Coach Backend Running"}


if __name__ == "__main__":
    app.run(debug=True)
