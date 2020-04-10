import sqlite3
import sys
import pprint

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#login required
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Configure SQLite database
conn = sqlite3.connect('peacock.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Create table
# db.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')


@app.route('/')
def index():
	# return "Hello World!"
	# Insert a row of data
	# db.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
	# conn.commit()
	# conn.close()
	return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":

		# Ensure username was submitted
		if not request.form.get("username"):
			flash('Please enter username')
			return render_template("register.html", email=request.form.get("email"))

		# Ensure password was submitted
		elif not request.form.get("email"):
			flash('Please enter email')
			return render_template("register.html", username=request.form.get("username"))

		# Ensure password was submitted
		elif not request.form.get("password"):
			flash('Please enter password')
			return render_template("register.html", username=request.form.get("username"), email=request.form.get("email"))

		# Ensure confirmation password was submitted
		elif not request.form.get("confirmation"):
			flash('Please re-type password')
			return render_template("register.html", username=request.form.get("username"), email=request.form.get("email"))

		if request.form.get("confirmation") != request.form.get("password"):
			flash('password fields must match')
			return render_template("register.html", username=request.form.get("username"), email=request.form.get("email"))

		# ok things have checked out, lets hash this password
		hash = generate_password_hash(request.form.get("password"))
		username = request.form.get("username")
		email = request.form.get("email")

		# now insert stuff into db

		# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

		c.execute("INSERT INTO users (username, email, hash) VALUES (?,?,?)",
				  (username, email, hash))
		conn.commit()

		# route to event creation page
		return render_template("newevent.html")

	# User reached route via GET (as by clicking a link or via redirect)
	else:
		return render_template("register.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
	currentUser = int(session["user_id"])

	pprint.pprint("HELO!" + str(currentUser))
	#print("curr user? ", currentUser)

	c.execute("SELECT username FROM users WHERE id=?", (currentUser,))
	user = c.fetchone()['username']

	print(str(user))

	if request.method == "POST":
		return render_template("dashboard.html")

	else:
		pprint.pprint(currentUser)
		return render_template("dashboard.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():

	# Forget any user_id
	session.clear()

	# User reached route via POST (as by submitting a form via POST)
	if request.method == "POST":

		grabEmail = request.form.get("email")

		# Ensure username was submitted
		if not request.form.get("email"):
			flash('Please enter in email address')
			return render_template("login.html")

		# Ensure password was submitted
		elif not request.form.get("password"):
			flash('Please enter in password')
			return render_template("login.html", email=grabEmail)

		# Query database for username
		# cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})

		c.execute("SELECT * FROM users WHERE email=:email", {"email": grabEmail})
		# rows = (c.fetchall())

		#c.execute('SELECT * FROM users')

		records = c.fetchall()

		print("Total rows are:  ", len(records))

		for row in records:
			print("id: ", row[0])
			print("username: ", row[1])
			print("email: ", row[2])
			print("hash: ", row[3])
			print("\n")
			print("try to index BY NAME: " + row['username'])
			
		# print (r)

		# print (r.keys())

		# print (r['username'])

		# print("LENGTH")

		# Ensure username exists and password is correct
		if len(records) != 1 or not check_password_hash(records[0]["hash"], request.form.get("password")):
			flash('invalid username and/or password')
			return render_template("login.html")

		# Remember which user has logged in
		#print("SESSION? " + str(rows[0][0]))
		print("RECORDS " + str(records[0]['id']))
		session["user_id"] = records[0]['id']

		# Redirect user to home page
		return redirect("/dashboard")

	# User reached route via GET (as by clicking a link or via redirect)
	else:
		return render_template("login.html")
