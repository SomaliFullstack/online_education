from flask import Flask
from flask_session import Session
from datetime import timedelta
import os

app = Flask(__name__)

# Secret key for session security
app.secret_key = "designer32"

# Session configuration
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config['SESSION_FILE_DIR'] = './flask_session'
app.config["SESSION_COOKIE_NAME"] = "session"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)

# Directory for storing session files
SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), '..', 'flask_session')
os.makedirs(SESSION_FILE_DIR, exist_ok=True)
app.config["SESSION_FILE_DIR"] = SESSION_FILE_DIR

# Initialize Flask-Session
Session(app)

# Import routes (after app is created)
from app.public.public_view import erorpage
