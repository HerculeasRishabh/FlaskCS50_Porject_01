import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def import_books ():
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    books_csv = open ("books.csv")

    csv_reader = csv.reader(books_csv)

    for isbn, title, author, year in csv_reader:
        try:
            db.execute("INSERT INTO BOOKS VALUES (:isbn, :title, :author, :year)",
                    {"isbn" : isbn, "title" : title, "author" : author, "year" : year})
            print ("Insert Success")
        except Exception as err:
            print ("Insert Failuer")
            print(isbn, title, author, year)
            print (err)
    db.commit()


if __name__ == "__main__":
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL not set")
    import_books()

