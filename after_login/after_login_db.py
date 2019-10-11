import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

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

if __name__ == "__main__":
    my_book = Books(book_isbn="1234")
    books = my_book.get_books()
    print (books)