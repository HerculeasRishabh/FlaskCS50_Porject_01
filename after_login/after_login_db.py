import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from datetime import datetime

class Books:
    def __init__(self, book_isbn="", book_title="", book_author="", book_year=None):
        self.book_isbn=book_isbn
        self.book_title=book_title
        self.book_author=book_author
        self.book_year=book_year

    def get_books(self):
        if not os.getenv("DATABASE_URL"):
            raise("DATABASE_URL is not set")

        engine = create_engine(os.getenv("DATABASE_URL"))
        db = scoped_session(sessionmaker(bind=engine))

        try:
            if self.book_year is not None:
                books = db.execute("SELECT * FROM BOOKS WHERE ISBN LIKE :isbn AND TITLE LIKE :title AND AUTHOR LIKE :author AND YEAR = :year",
                            {"isbn" : "%"+self.book_isbn+"%", "title" : "%"+self.book_title+"%", 
                            "author" : "%"+self.book_author+"%", "year" : self.book_year}).fetchall()
            else:
                books = db.execute("SELECT * FROM BOOKS WHERE ISBN LIKE :isbn AND TITLE LIKE :title AND AUTHOR LIKE :author",
                            {"isbn" : "%"+self.book_isbn+"%", "title" : "%"+self.book_title+"%", 
                            "author" : "%"+self.book_author+"%"}).fetchall()

           # for book in books:
           #     print (book)
            print ("Success")
        except Exception as err:
            print ("ERROR: occured during db.execute")
            print(err)
        return books if books is not None else None

    def get_ISBN_Book(self):
        if not os.getenv("DATABASE_URL"):
            raise("DATABASE_URL is not set!")

        engine = create_engine(os.getenv("DATABASE_URL"))
        db = scoped_session(sessionmaker(bind=engine))

        try:
            book = db.execute("SELECT * FROM BOOKS WHERE ISBN = :isbn", {"isbn" : self.book_isbn}).fetchone()
        except Exception as err:
            print ("ERROR while fetching book with isbn")
            print (err)
        return book if book is not None else None


class Book_Review:
    def __init__(self, book_isbn, user_email='', user_rating='', user_review='', review_timestamp=None):
        self.user_email=user_email
        self.book_isbn=book_isbn
        self.user_rating=user_rating
        self.user_review=user_review
        self.review_timestamp=review_timestamp

    def insert_user_review(self):
        if not os.getenv("DATABASE_URL"):
            return ("DATABASE_URL is not set!")

        engine = create_engine(os.getenv("DATABASE_URL"))
        db = scoped_session(sessionmaker(bind=engine))

        try:
            result = db.execute("INSERT INTO BOOK_REVIEWS(USER_EMAIL, BOOK_ISBN, USER_RATING, USER_REVIEW) VALUES (:user_email, :book_isbn, :user_rating, :user_review)",
                    {"user_email" : self.user_email, "book_isbn" : self.book_isbn, "user_rating" : self.user_rating, "user_review" : self.user_review})
        except Exception as err:
            print ("Error in inserting user review")
            print(err)
        print (result)
        db.commit()
        return result if result is not None else None

    def select_user_review(self):
        if not os.getenv("DATABASE_URL"):
            raise("DATABASE_URL is not set!")

        engine = create_engine(os.getenv("DATABASE_URL"))
        db = scoped_session(sessionmaker(bind=engine))

        try:
            all_reviews = db.execute("SELECT * FROM BOOK_REVIEWS WHERE BOOK_ISBN = :book_isbn", {"book_isbn" : self.book_isbn}).fetchall()
        except Exception as err:
            print("Error occured while fetcing user reviews")
            print(err)
        print (all_reviews)
        print (all_reviews[0][4].date())
        return all_reviews if all_reviews is not None else None

if __name__ == "__main__":
    my_review = Book_Review()