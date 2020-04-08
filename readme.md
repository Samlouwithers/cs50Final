reference this guide for flask/python setup

https://www.patricksoftwareblog.com/steps-for-starting-a-new-flask-project-using-python3/

you need python3

To run virtual enviornment:
$ source venv/bin/activate

to go back to regular terminal:

(venv) $ deactivate

to run dev server (configure venv)
(venv) $ export FLASK_APP=app.py
(venv) $ flask run


go to: http://localhost:5000

to access db

(venv) $ sqlite3 rsvp.db

to view schema

sqlite> .schema