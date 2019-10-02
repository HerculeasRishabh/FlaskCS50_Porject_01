import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def fetch_test():
    # The format of DATABASE_URL is: 
    #   <db_engine>://<user_name>:<password>@<host_name>/<database_name>
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    test_rows = db.execute("SELECT * FROM test").fetchall()

    for row in test_rows:
        print (f"ID: {row.id} --- Name: {row.name}")

if __name__ == "__main__":
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL not set")
    fetch_test()