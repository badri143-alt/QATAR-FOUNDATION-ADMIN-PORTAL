from flask import Flask, send_file
from flask_login import LoginManager
from models import db, Admin
from routes import bp
import os

app = Flask(__name__)

# Secret key
app.config["SECRET_KEY"] = "secret123"

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init DB
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Register Routes
app.register_blueprint(bp)

# Create DB Tables
with app.app_context():
    db.create_all()

BASE_DIR = os.path.dirname(__file__)

# Frontend Routes
@app.route("/")
def home():
    return send_file(os.path.join(BASE_DIR, "sky", "admin.html"))

@app.route("/admin.css")
def css():
    return send_file(os.path.join(BASE_DIR, "sky", "admin.css"))

@app.route("/admin.js")
def js():
    return send_file(os.path.join(BASE_DIR, "sky", "admin.js"))

if __name__ == "__main__":
    app.run(debug=True)