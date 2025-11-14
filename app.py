import os
import jwt
import bcrypt
from lib.authentication_utility import valid_password, hash_password, compare_password_hash
from datetime import datetime, timezone, timedelta, date
import calendar
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
from lib.booking_repository import BookingRepository
from lib.booking import Booking

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
    return render_template('login.html', error=False)

@app.route('/testlogin', methods=['GET'])
@token_required
def test_login(user):
    return user.name

# @app.route('/login', methods=['POST'])
# def user_login():
#     connection = get_flask_database_connection(app)
#     user_repo = UserRepository(connection)
    
#     user_email = request.form['email']
#     user_password = request.form['password']

@app.route('/signup', methods=['GET'])
def serve_signup():
    return render_template('signup.html', error=False)

@app.route('/spaces', methods=['GET'])
@token_required
def get_space(user):
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    
    # Get date filter parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # If no dates provided, show all spaces
    if not start_date_str or not end_date_str:
        spaces = space_repo.all()
        return render_template('spaces.html', spaces=spaces, logged_in=isinstance(user, User), 
                             start_date=start_date_str, end_date=end_date_str)
    
    # Parse dates
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        spaces = space_repo.all()
        return render_template('spaces.html', spaces=spaces, logged_in=isinstance(user, User),
                             start_date=start_date_str, end_date=end_date_str, 
                             error="Invalid date format")
    
    # Validate date range
    if start_date > end_date:
        spaces = space_repo.all()
        return render_template('spaces.html', spaces=spaces, logged_in=isinstance(user, User),
                             start_date=start_date_str, end_date=end_date_str,
                             error="Check-out date must be after check-in date")
    
    # Filter spaces by availability
    availability_repo = AvailabilityRepository(connection)
    all_spaces = space_repo.all()
    filtered_spaces = []
    
    for space in all_spaces:
        availabilities = availability_repo.find_by_space_id(space.id)
        
        # Expand availability ranges to ISO date set
        available_dates = set()
        for avail in availabilities:
            current = avail.start_date
            while current <= avail.end_date:
                available_dates.add(current.isoformat())
                current += timedelta(days=1)
        
        # Check if all requested dates are available
        current = start_date
        all_dates_available = True
        while current <= end_date:
            if current.isoformat() not in available_dates:
                all_dates_available = False
                break
            current += timedelta(days=1)
        
        if all_dates_available:
            filtered_spaces.append(space)
    
    return render_template('spaces.html', spaces=filtered_spaces, logged_in=isinstance(user, User),
                         start_date=start_date_str, end_date=end_date_str)

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

    # Build available dates set from availability repository
    availability_repo = AvailabilityRepository(connection)
    availabilities = availability_repo.find_by_space_id(id)

    # Expand availability ranges into individual ISO dates using stdlib
    available_dates = set()
    for period in availabilities:
        start = period.start_date
        end = period.end_date

        if isinstance(start, str):
            start = date.fromisoformat(start)
        if isinstance(end, str):
            end = date.fromisoformat(end)

        d = start
        while d <= end:
            available_dates.add(d.isoformat())
            d = d + timedelta(days=1)

    # Determine month/year to show (allow ?year=YYYY&month=MM)
    try:
        month = int(request.args.get('month') or date.today().month)
        year = int(request.args.get('year') or date.today().year)
    except Exception:
        month = date.today().month
        year = date.today().year

    # Build month grid (list of weeks, each week is list of day dicts)
    def build_month_grid(year, month, available_iso_set):
        cal = calendar.Calendar(firstweekday=6)  # Week starts on Sunday
        weeks = []
        for week in cal.monthdatescalendar(year, month):
            week_cells = []
            for d in week:
                iso = d.isoformat()
                in_month = (d.month == month)
                available = iso in available_iso_set
                week_cells.append({
                    'date': d,
                    'iso': iso,
                    'in_month': in_month,
                    'available': available,
                    'day': d.day,
                })
            weeks.append(week_cells)
        return weeks

    calendar_weeks = build_month_grid(year, month, available_dates)

    month_name = calendar.month_name[month]

    # compute previous and next month/year for server-side navigation
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    base_path = request.path

    return render_template(
        'single_space_id.html',
        space=space,
        host_name=host_name,
        logged_in=isinstance(user, User),
        calendar_weeks=calendar_weeks,
        calendar_month=month,
        calendar_year=year,
        calendar_month_name=month_name,
        calendar_prev_month=prev_month,
        calendar_prev_year=prev_year,
        calendar_next_month=next_month,
        calendar_next_year=next_year,
        calendar_base_path=base_path,
    )

@app.route('/signup', methods=['POST'])
def create_user():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if isinstance(repository.find_by_email(email), User):
        # account already exists
        return render_template('signup.html', errormsg = "Email already in use!", error=True), 202

    #TODO - password validation
    if not valid_password(password):
        print("posting")
        return render_template('signup.html', errormsg = "Include 1+ !£$% character", error=True), 202
    hashed_password = hash_password(password)

    repository.create(User(None, name, email, hashed_password.decode('utf-8')))

    return render_template('login.html', error=False), 201

@app.route('/login', methods=['POST'])
def attempt_login():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    email = request.form['email']
    password = request.form['password'].strip(" ")

    if not isinstance(repository.find_by_email(email), User):
        print("email wrong?")
        return render_template('login.html', errormsg="Wrong credentials!", error=True)
    
    user = repository.find_by_email(email)
    password_hash = user.password_hash
    if compare_password_hash(password, password_hash) != True:
        print("password wrong:", password)
        return render_template('login.html', errormsg="Wrong credentials!", error=True)
    
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


@app.route('/spaces/<int:id>/book', methods=['GET', 'POST'])
@token_required
def book_space(user,id):
    """Placeholder booking route: echoes selected dates for the given space.

    Accepts either GET (query params `dates=...`) or POST (form `dates` fields).
    """
    if not isinstance(user, User):
        return redirect(url_for('serve_login'))
    if request.method == 'POST':
        dates = request.form.getlist('dates')
    else:
        dates = request.args.getlist('dates')

    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    space = space_repo.find(id)

    return render_template('book_placeholder.html', space=space, dates=dates)


# this displays the bookings to the host  and the bookings that have been rented by the same user
@app.route('/requests', methods=['GET'])
@token_required
def get_bookings(user):
    if not isinstance(user, User):
        return redirect(url_for('serve_login'))
    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    hosted_bookings = booking_repo.get_by_host(user.id)
    rented_bookings = booking_repo.get_by_renter(user.id)
    return render_template('requests.html', rented_bookings = rented_bookings, hosted_bookings = hosted_bookings )


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))