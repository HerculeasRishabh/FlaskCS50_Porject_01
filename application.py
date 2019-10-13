import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from before_login.before_login_db import Before_Login_Logic
from after_login.after_login_db import Books, Book_Review

# None to string converter
#xstr = lambda s : s or ""
xInt = lambda i : None if i == '' else i

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

#
# GET Requests
#
@app.route("/index")
def index():
    if 'user' in session:
        session.pop("user", None)
    return render_template("index.html")

@app.route("/register")
def register():
    if 'user' in session:
        session.pop("user", None)
    return render_template("register.html")

@app.route("/login")
def login():
    if 'user' in session:
        session.pop("user", None)
    return render_template("login.html")

#
# POST Requests
#
@app.route("/register_user", methods=["POST"])
def register_user():
    if 'user' in session:
        session.pop("user", None)
    user_name = request.form.get('user_name')
    user_email = request.form.get('user_email')
    user_psswd = request.form.get('user_psswd')

    user = Before_Login_Logic(user_name=user_name, user_email=user_email, user_psswd=user_psswd)
    user.register_user()

    return render_template("index.html", Message="Registration Success")

@app.route("/login_user", methods=["POST"])
def login_user():
    if 'user' in session:
        session.pop("user", None)
    user_email = request.form.get("user_email")
    user_psswd = request.form.get("user_psswd")

    user_data = Before_Login_Logic(user_email=user_email, user_psswd=user_psswd)
    user = user_data.login_user()

    if user is not None:
        session['user'] = user
        return render_template("search.html", user=user)
    return render_template("index.html", Message="User Name/Password Invalid")

#
# After Login
#

@app.route("/search", methods=["GET"])
def search():
    if 'user' in session:
        return render_template("search.html", user=session['user'])
    else:
        return render_template("index.html", Message="Please login First")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if 'user' in session:
        session.pop("user", None)
        return render_template("index.html", Message="Logout Successful")
    else:
        return render_template("index.html", Message="User already logged out")


@app.route("/search_books", methods=["POST"])
def search_books():
    if 'user' not in session:
        return render_template("index.html", Message="Please login First")
    
    book_isbn = request.form.get("book_isbn")
    book_title = request.form.get("book_title")
    book_author = request.form.get("book_author")
    book_year = xInt(request.form.get('book_year'))

    print("Book_Year: ", book_year, type(book_year))
    book_data = Books(book_isbn=book_isbn, book_title=book_title, 
                    book_author=book_author, book_year=book_year)

    books = book_data.get_books()

    return render_template("search_books.html", books=books, user=session['user'])

@app.route("/find_book/<string:isbn>")
def find_book(isbn):
    if 'user' not in session:
        return render_template("index.html", Message="Please login First")
    
    book = Books(book_isbn=isbn)
    book_data = book.get_ISBN_Book()

    return render_template("book_review.html", book_data=book_data, user=session['user'])

@app.route("/submit_review", methods=["POST"])
def submit_review():
    if 'user' not in session:
        return render_template('index.html', Message="Please login First")

    user_rating = request.form.get("rating")
    user_review = request.form.get("user_review")
    book_isbn = request.form.get("book_isbn")

    print (session['user'][1], book_isbn, user_rating, type(user_review))
    
    user_review_obj = Book_Review(session['user'][1], book_isbn, user_rating, user_review)
    review_result = user_review_obj.insert_user_review()

    print(review_result)

    return render_template("test.html", user=session['user'])


@app.route("/test")
def test():
    return render_template("test.html", user=session['user'])