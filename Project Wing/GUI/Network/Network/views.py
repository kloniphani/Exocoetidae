"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import send_from_directory
from Network import app

import os

@app.route('/')
@app.route('/network')
def network():
	"""Renders the Network Map page."""
	return render_template(
		'network.html',
		title='Network Map',
		year=datetime.now().year,
	)

@app.route('/home')
def home():
	"""Renders the home page."""
	return render_template(
		'index.html',
		title='Home Page',
		year=datetime.now().year,
	)

@app.route('/contact')
def contact():
	"""Renders the contact page."""
	return render_template(
		'contact.html',
		title='Contact',
		year=datetime.now().year,
		message='Your contact page.'
	)

@app.route('/about')
def about():
	"""Renders the about page."""
	return render_template(
		'about.html',
		title='About',
		year=datetime.now().year,
		message='Your application description page.'
	)

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.ico')

