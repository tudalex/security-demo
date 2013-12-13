#!/usr/bin/env python
from flask import Flask, session, redirect, url_for, escape, request


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
	data = ""
	if request.method == 'POST':
		data = request.form['data']
	return '''
	<form action="" method="post">
	<p><textarea cols=200 rows=40 name="data">'''+data+'''</textarea></p>
	<p><input type="submit" value="Run"></p>
	</form>
	<div>'''+data+'''
	'''



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=3000)
