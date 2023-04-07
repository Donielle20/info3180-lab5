"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import json
import jwt
import psycopg2
from app import app
from flask import jsonify, render_template, request, jsonify, send_file, send_from_directory, url_for
import os
from app import db
from app.models import Movies
from .forms import MovieForm
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    myform = MovieForm()
    if request.method == 'POST':
        if myform.validate_on_submit():
            title = myform.title.data
            description = myform.description.data
            poster = myform.poster.data

            filename = secure_filename(poster.filename)

            movie = Movies(title=title, description=description, poster=filename)
            db.session.add(movie)
            db.session.commit()

            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # dic = {}
            # dic = {
            #     "message": "Movie Successfully added",
            #     "title": title,
            #     "poster": filename,
            #     "description": description
            # }

            return jsonify({"message": "Movie Successfully added","title": title,"poster": filename,"description": description})
        else:
            return jsonify({"errors": form_errors(myform)})

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), filename)

def connect_db():
    return psycopg2.connect(host="localhost", database="lab5", user="lab5", password="Loveisdeath123321")

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})