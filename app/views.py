from flask import render_template, request
from app import app

@app.route('/')
def homepage():
	name = request.args.get('name')
	number = request.args.get('number')
	if not name:
		name = '<unknown>' #http://127.0.0.1:5000/?name=Charlie
	return render_template('homepage.html', name=name, number=number)
