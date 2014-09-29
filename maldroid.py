# all the imports
import os
import sqlite3
from time import gmtime, strftime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug import secure_filename

# Create and Configure the flask app
app = Flask(__name__)
UPLOAD_FOLDER = './uploads/apk_samples'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','jpeg','gif']) # Default upload ext set
app.config.from_object(__name__)
app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'maldroid.db'),
	DEBUG = True,
	UPLOAD_FOLDER = UPLOAD_FOLDER
	#SECRET_KEY = 'd3v3lopm3nt_k3y',
	#USERNAME = 'admin',
	#PASSWORD = 'default'
	))


""" Connect to the sqlite db """
def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv


# Open the DB connection if it doesn't already exist
def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


# Close the DB connection at the end of requests.
@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


# Setup the database.
def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


# At some point, this needs to be refined, to ensure that the
# file itself is appropriate to be on our server, as opposed to
# having a proper file extension :P
def allowed_file(fname):
	return '.' in fname and fname.split('.')[-1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			fname = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
			return redirect(url_for('report', fname=fname))
	return redirect(url_for('error'))


#@app.route('/report', methods=['GET','POST'])
@app.route('/report')
def report():
	apkname = request.args.get('fname')
	return redirect(url_for('home'))


@app.route('/')
@app.route('/home')
def home():
	#db = get_db()
	#cur = db.execute('select title, text, timestamp from entries order by id desc')
	#entries = cur.fetchall()
	return render_template('index.html')

# Route for Contact form
@app.route('/contact')
def contact():
	return render_template('contact.html')

# Route for About form
@app.route('/about')
def about():
	return render_template('about.html')

# Generic error page
@app.route('/error')
def error():
	return render_template('error.html')



# This is the default manner in which to uplpoad a file in flask.  Right
# now I'm just following the tutorial here: http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# but at some point we'll want to restrict this to very very very specifically
# android APKs, so that our server isn't being flooded with files :S



"""
@app.route('/add', methods=['POST'])
def add_entry():
	current_time = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute('insert into entries (title, text, timestamp) values (?, ?, ?)',
		[request.form['title'], request.form['text'], current_time])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for("show_entries"))
"""

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Logon Credentials'
		else:
			session['logged_in'] = True
			flash('You have been successfully logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)
"""

"""
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
"""


if __name__ == '__main__':
	

	app.run()


