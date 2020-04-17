#Peacocktopia RSVP app

*This is a web based application built in Python 3 with flask and jinja*

*This is a web app that allows users to create events with details, a neat downloadable PDF for each event, and email updates, with a unique RSVP ID that their guests can easily RSVP online with.*

##orignal set up notes

Reference this guide for flask/python setup
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

## index page
Users begin with the login page on Peacocktopia RSVP. There are 3 options: Login, Register, RSVP.

### Register
Register brings users to the Register page. They are requested to fill in 4 form fields: Name, email, and create password (followed by re-typing that password). There is a requirement for each field to be submited and validation that shows up when users try so submit without filling it out via a flash error. Additionally, there is validation checking that the password and confirm password fiels match. Each user info is placed in the marty.db user's table as a user with a unique primary key ID and their passwords hashed. 

Upon completing the for, users are directed to now log in properly. Once they log in, they are directed to the dashboard. The dashboard page contains a message saying you don't have any events! would you like to set one up? This opens the event creation form.

### Login
The login route brings users to the login page. There are requirements to validate users against marty.db's users table and their passwords using hash. A session ID is created and set to keep the user logged in properly. Future state, set up a forgot password workflow.

### RSVP
If a guest has recieved a host's unique ID to RSVP by, the directs them to the form which asks for the unique ID. The unique ID checks agains marty.db's events table to see if that ID exists, then brings up the host and party name on the guest info page, where guests are prompted to enter their first name, last name, and email. The email is for an enhancement feature where the host can batch email their guests of any event updates, or notifications. Once the guest has submitted their RSVP they are directed back to the guest Info RSVP screen and told they are all set and is there another guest they would like to RSVP for. Meanwhile, the host has already been sent a notificaiton email stating that a guest has just RSVP'd to their specific event. This email includes the guest name and name of event to help keep things straight. 

RSVP sends guest information to the marty.db guests table. The guests table includes a primary Key per guest and a foreign key connecting to the event id for later retrieval. 

future state: email guests a reminder email 2 days before the event reminding them of the party's address, and any other event information.


## Dashboard
*Once a user logs in, they are brought to the dashboard*

If a user does not have any events, the page welcomes the user by name, and then prompts the user to create a new event. If the user already has an event created, they will see the event header containing the event name. They can select the event header to toggle a dropdown of all the event details. The details of the event are: 
- date of event
- Address
- theme
- registry
- event code

If guests have RSVP'd, there will be a table (with guest count) that has all the guest info per that specific event. at the bottom of this details drawer, there are two options: Edit and PDF.

Future state: add a "delete event" option and an "email" option where hosts can email all guests of any updates. 

### Edit
Edit sends the user to the edit this event workflow. The user is directed to a pre-filled form with that specific event's detials where they can update information. Any information submitted instantly updates the marty.db events table aand reflects instantly when returning to the dashboard page. 

### PDF
PDF utilizes an html template and pdfgen to create a PDF dynamically of the current event's details and guest list. It is downloaded instantly as an attachment. The user does not leave the dashboard page. 

## Create New Event
The create New event sends the user to a form where they fill out information about their new event. These fields are: 
- Event Name
- Event Date
- Event address
- Event Theme
- Event Registry

Additionally, a unique 6 digit string is created with a combination of letters and numbers and assigned to the event. All of these are stored in the marty.db events table. The event has a unique ID primary key, and a foreign key user id that connects to the users creating the event.

Upon completing the create event workflow, the user is directed back to the dashboard where they are given a confrimation flash message including the name of their new event and the ID. 

future state: send user an email at this time confirming the creation of their new event and especially the new unique ID for the event they can give their guests to RSVP with. 

Other future state ideas: add options for additional form fields that the host can requests of their guests. For example, hosts can ask their guests if they are bringing food, if so what. etc. 

## log out
Ends session and logs user out. 



