# Project 1

Web Programming with Python and JavaScript

To remove any file from being added to the git repository add the file name into
.gitignore file in the base repository directory.

Make sure to export the following environment variables before you run the app

export FLASK_APP=application.py
export FLASK_DEBUG=1


# GoodReads application keys
key: fiUbyOw3gaggKRlcSRhwTg
secret: 1I8JELpQmUxb92ZhulkuDOMtyZ10CaRUz5ZHmVVmFh4

# Table schema for Users
CREATE TABLE PROJECT_1_USERS (
USER_NAME VARCHAR(50) NOT NULL,
USER_EMAIL VARCHAR(100) PRIMARY KEY NOT NULL,
USER_PASSWORD VARCHAR(30) NOT NULL,
CONSTRAINT PROPER_EMAIL CHECK (USER_EMAIL ~* '^[A-Za-z0-9_.%-]+@[A-Za-z0-9_-]+[.][A-Za-z]+$')
);
