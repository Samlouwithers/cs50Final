import sqlite3

from flask import Flask, redirect, render_template, request, session
 
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure SQLite database
conn = sqlite3.connect('rsvp.db', check_same_thread=False)
db = conn.cursor()

# Create table
#db.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')


 
@app.route('/')
def index():
	#return "Hello World!"
	# Insert a row of data
	db.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
	conn.commit()
	return render_template("index.html")