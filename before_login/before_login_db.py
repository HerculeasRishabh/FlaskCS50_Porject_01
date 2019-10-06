import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Before_Login_Logic:
    def __init__(self, user_email, user_psswd, user_name=None):
        self.user_name = user_name
        self.user_email = user_email
        self.user_psswd = user_psswd

    def register_user (self):
        if not os.getenv("DATABASE_URL"):
            raise ("DATABASE_URL is not set!")

        engine = create_engine(os.getenv("DATABASE_URL"))
        db = scoped_session(sessionmaker(bind=engine))

        try:
            result = db.execute("INSERT INTO PROJECT_1_USERS VALUES (:user_name, :user_email, :user_psswd)", 
                        {"user_name" : self.user_name, "user_email" : self.user_email, "user_psswd" : self.user_psswd})
            print (result)
            db.commit()
        except Exception as err:
            print ("ERROR encountered while inserting into PROJECT_1_USERS")
            print (err)

    def login_user (self):
        if not os.getenv("DATABASE_URL"):
            raise ("DATABASE_URL is not set!")

        engine = create_engine(os.getenv("DATABASE_URL"))
        db = scoped_session(sessionmaker(bind=engine))

        try:
            result = db.execute("SELECT * FROM PROJECT_1_USERS WHERE USER_EMAIL = :user_email AND USER_PASSWORD = :user_psswd",
                            {"user_email" : self.user_email, "user_psswd" : self.user_psswd}).fetchone()
            #print (result)
        except Exception as err:
            print (err)
        # [on_true] if [expression] else [on_false]
        return result if result is not None else None

if __name__ == "__main__":
    user = Before_Login_Logic("risha@gmail.com", "123")
    user.login_user()