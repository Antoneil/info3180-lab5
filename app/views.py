import os
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app import app, db
from .forms import MovieForm
from .models import Movie

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    form = MovieForm()
    # Validate file upload on submit
    if form.validate_on_submit():
        # Get file data and save to your uploads folder
        file = form.poster.data

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))

            flash('File Saved', 'success')
            return redirect(url_for('home'))  # Redirect to the home page

        else:
            flash('Invalid file format. Please upload only jpg or png files.', 'danger')
    return render_template('upload.html', form=form)

@app.route('/uploads/<filename>')
def get_image(filename):
    uploads_folder = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads_folder, filename)

def get_uploaded_images():
    rootdir = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
    uploaded_images = []

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            uploaded_images.append(file)

    return uploaded_images

upload_folder = app.config['UPLOAD_FOLDER']
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route('/movies')
def get_movies():
    all_movies = Movie.query.all()  # Retrieve all movies from the database
    return render_template('movies.html', movies=all_movies)
    
    return jsonify(movie_data)  # Return movie data in JSON format

# Route for serving static text file
@app.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

# Function to collect form errors from Flask-WTF
def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)
    return error_messages

# After request handler to add headers
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# Error handler for 404 page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Route for processing movie submissions
@app.route('/api/v1/movies', methods=['POST'])
def submit_movies():
    form = MovieForm()

    if request.method == 'POST' and form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            poster='your-uploaded-movie-poster.jpg'  # Replace with actual filename
        )
        db.session.add(movie)
        db.session.commit()

        poster_file = request.files['poster']
        poster_filename = secure_filename(poster_file.filename)
        # Make sure UPLOAD_FOLDER is properly configured in your Flask app config
        poster_file.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))

        return jsonify({
            "message": "Movie Successfully added",
            "title": form.title.data,
            "poster": poster_filename,
            "description": form.description.data
        })

    errors = form_errors(form)
    return jsonify({"errors": errors})


    