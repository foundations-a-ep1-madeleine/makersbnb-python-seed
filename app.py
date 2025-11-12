import os
from flask import Flask, request, render_template, jsonify
from lib.database_connection import get_flask_database_connection
from lib.availability_repository import AvailabilityRepository
from lib.availability import Availability
from lib.space_repository import SpaceRepository
from lib.space import Space
from lib.user_repository import UserRepository
from lib.date_serialization import string_to_date


# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

@app.route('/login', methods=['GET'])
def serve_login():
    return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def user_login():
#     connection = get_flask_database_connection(app)
#     user_repo = UserRepository(connection)
    
#     user_email = request.form['email']
#     user_password = request.form['password']

@app.route('/signup', methods=['GET'])
def serve_signup():
    return render_template('signup.html')

@app.route('/spaces', methods=['GET'])
def get_space():
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    spaces = space_repo.all()
    return render_template('spaces.html', spaces=spaces)

@app.route('/spaces', methods=['POST'])
def create_space():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = Space(None, request.form['name'], request.form['description'], request.form['price'], request.form['user_id'])
    space = repository.create(space)
    return "Space added successfully"

@app.route('/spaces/<id>', methods=['GET'])
def get_space_by_user_id(id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find(id)
    return render_template('single_space_id.html', space=space)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/spaces/<int:id>/availability', methods=['GET'])
def get_space_availability(id):
    connection = get_flask_database_connection(app)
    repository = AvailabilityRepository(connection)

    availabilities = repository.find_by_space_id(id)

    availabilities_data = [
        availability.to_dict() for availability in availabilities
    ]
    
    return jsonify(availabilities_data)

@app.route('/spaces/availability', methods=['POST'])
def create_space_availability():
    connection = get_flask_database_connection(app)
    repository = AvailabilityRepository(connection)
    repository.create(Availability(None, string_to_date(request.form['start_date']), string_to_date(request.form['end_date']), request.form['space_id']))
    return "Availability added"

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
