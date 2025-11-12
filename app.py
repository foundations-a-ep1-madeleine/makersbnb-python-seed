import os
import jwt
import bcrypt
from functools import wraps
from flask import Flask, request, render_template, jsonify
from lib.database_connection import get_flask_database_connection
from lib.availability_repository import AvailabilityRepository
from lib.availability import Availability
from lib.space_repository import SpaceRepository
from lib.user import User
from lib.user_repository import UserRepository
from lib.space import Space
from lib.date_serialization import string_to_date

# Create a new Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "wow_so_secret"

# User Authentication #

# Returns a salted, hashed password
def hash_password(password):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)

# Takes in a plain text password and a hashed password and returns a boolean
# depending on if they are the same
def compare_password_hash(entered_password, hashed_password):
    password_bytes = entered_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            return jsonify({'message': 'Token missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            connection = get_flask_database_connection()
            repo = UserRepository(connection)

            user = repo.find(data.user_id)
            
        except:
            return jsonify({'message': 'Token invalid'}), 401

        return f(user, *args, **kwargs)

    return decorated

# Routes #
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