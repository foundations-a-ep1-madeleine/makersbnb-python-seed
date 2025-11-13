import os
import jwt
import bcrypt
from lib.authentication_utility import valid_password, hash_password, compare_password_hash
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import Flask, request, render_template, jsonify, url_for, redirect, make_response
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

#== User authentication ==#
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            return f(None, *args, **kwargs)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            connection = get_flask_database_connection(app)
            repo = UserRepository(connection)

            user = repo.find(data['user_id'])
            
        except Exception as e:
            return f(None, *args, **kwargs)

        return f(user, *args, **kwargs)

    return decorated

#== Routes ==#
@app.route('/login', methods=['GET'])
@token_required
def serve_login(user):
    if isinstance(user, User):
        return redirect(url_for('get_space'))
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
@token_required
def get_space(user):
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    spaces = space_repo.all()
    return render_template('spaces.html', spaces=spaces, logged_in=isinstance(user, User))

@app.route('/spaces', methods=['POST'])
def create_space():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = Space(None, request.form['name'], request.form['description'], request.form['price'], request.form['user_id'])
    space = repository.create(space)
    return "Space added successfully"

@app.route('/spaces/<int:id>', methods=['GET'])
@token_required
def get_space_by_user_id(user, id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find(id)
    # route-level lookup: fetch host name to display instead of numeric id
    user_repo = UserRepository(connection)
    host = None
    if space and getattr(space, 'user_id', None) is not None:
        host = user_repo.find(space.user_id)
    host_name = host.name if host else None

    return render_template('single_space_id.html', space=space, host_name=host_name, logged_in=isinstance(user, User))

@app.route('/signup', methods=['POST'])
def create_user():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if repository.find_by_email(email) != None:
        # account already exists
        return render_template('signup.html', error = "Please enter an email that isn't already in use!"), 202

    #TODO - password validation
    if not valid_password(password):
        return render_template('signup.html', error = "Please enter a valid password. > 7 characters, including 1 or more !£$%"), 202
    hashed_password = hash_password(password)

    repository.create(User(None, name, email, hashed_password.decode('utf-8')))

    return render_template('login.html'), 201

@app.route('/login', methods=['POST'])
def attempt_login():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    email = request.form['email']
    password = request.form['password'].strip(" ")

    if not isinstance(repository.find_by_email(email), User):
        print("email wrong?")
        return render_template('login.html', error = "One or more of your credentials was incorrect!")
    
    user = repository.find_by_email(email)
    password_hash = user.password_hash
    if compare_password_hash(password, password_hash) != True:
        print("password wrong:", password)
        return render_template('login.html', error = "One or more of your credentials was incorrect!")
    
    #password is right and email is right
    print("Success")
    token = jwt.encode({'user_id': user.id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
    response = make_response(redirect(url_for("get_index")))
    response.set_cookie('jwt_token', token)

    return response

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    response = make_response(redirect(url_for('serve_login')))
    response.set_cookie('jwt_token', '')

    return response

# == Your Routes Here ==

# GET /index
# Returns the homepage with all spaces
# Try it:
#   ; open http://localhost:5001/index
@app.before_request
def debug_db_name():
    conn = get_flask_database_connection(app)
    print("Connected to database:", conn._database_name())
    
@app.route('/index', methods=['GET'])
@token_required
def get_index(user):
    return redirect(url_for('get_space'))

@app.route('/', methods=['GET'])
def get_home():
    return redirect(url_for('get_space'))

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