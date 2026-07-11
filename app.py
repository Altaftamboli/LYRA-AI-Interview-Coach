from flask import Flask
from backend.config import Config
from backend.database import init_db
from backend.auth import auth_bp
from backend.routes import main_bp

app = Flask(__name__)

app.config.from_object(Config)

init_db(app)

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)


@app.route("/")
def home():
    return {"message": "AI Interview Coach Backend Running Successfully"}


if __name__ == "__main__":
    app.run(debug=True)
