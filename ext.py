from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SECRET_KEY'] = 'your_secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///your_database.db"
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg'}

db = SQLAlchemy(app)
login_manager = LoginManager(app)