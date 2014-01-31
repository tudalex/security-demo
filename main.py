#!/usr/bin/env python
from flask import Flask, session, redirect, url_for, escape, request, make_response
from flaskext.mysql import MySQL
import re

app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'placinta'
app.config['MYSQL_DATABASE_DB'] = 'security'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


attributes = ('id', 'username', 'name')

@app.route('/')
def index():
	return redirect(url_for('home'))


@app.route('/xss', methods=['GET','POST'])
def xss():
	response = make_response("<html><body>%s</body></html>" % request.values['data'])
	response.headers['X-XSS-Protection'] = '0'
	return response


@app.route('/home')
def home():
	if 'id' not in session:
		return redirect(url_for('login'))
	
	query = "SELECT name FROM users"
	cur = mysql.get_db().cursor()
	cur.execute(query)
	
	return '''
	<h1>Logged in as %s</h1>
	<a href="/profile">Edit profile</a>
	<br/>
	<ul>
	%s
	</ul>
	''' % (session['name'],
		   "\n".join(["<li>%s</li>" % line[0] for line in cur.fetchall()]))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		query = "SELECT %s FROM users where username='%s' and password='%s'" % (",".join(attributes), request.form['username'], request.form['password'])
		cur = mysql.get_db().cursor()
		cur.execute(query)
		data = cur.fetchone()
		if data:
			session.update(zip(attributes, data))
			return redirect(url_for('home'))
		
	return '''
	<form action="" method="post">
		<p>Username <input type="text" name="username"></p>
		<p>Password <input type="password" name="password"></p>
		<p><input type="submit" value="Login"></p>
	</form>
	'''


@app.route('/profile', methods=['GET', 'POST'])
def profile():
	if request.method == 'POST':
		session['name'] = request.form.get('name')
		query = "UPDATE users SET name='%s' where id=%d" % (re.escape(session['name']), session['id'])
		cur = mysql.get_db().cursor()
		cur.execute(query)
		mysql.get_db().commit()
	return '''
	<form action="" method="post">
		<p><input type="text" name="name" value="%s"></p>
		<p><input type="submit" value="Ok"></p>
	</form>
	''' % session['name']


@app.route('/logout')
def logout():
    for attr in attributes:
        session.pop(attr)
    return redirect(url_for('index'))


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=4000)
