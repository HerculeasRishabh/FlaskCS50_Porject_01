import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from before_login.before_login_db import Before_Login_Logic

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# GET Requests

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

# POST Requests

@app.route("/register_user", methods=["POST"])
def register_user():
    user_name = request.form.get('user_name')
    user_email = request.form.get('user_email')
    user_psswd = request.form.get('user_psswd')

    user = Before_Login_Logic(user_name, user_email, user_psswd)
    user.register_user()

    return render_template("index.html")

@app.route("login_user", method=["POST"])
def login_user():
    user_name = request.form.get("user_name")
    user_psswd = request.form.get("user_psswd")

    #TODO login function already created in before_login_db.py

