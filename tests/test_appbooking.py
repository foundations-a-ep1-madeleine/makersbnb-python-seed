import jwt
from datetime import datetime, timezone, timedelta
from lib.database_connection import get_flask_database_connection
from lib.booking_repository import BookingRepository
from app import app

def test_create_booking_for_available_date(db_connection, web_client):
    db_connection.seed("seeds/makersbnb.sql")

    token = jwt.encode({'user_id': 2, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
    web_client.set_cookie('jwt_token', token)

    response = web_client.post('/spaces/1/bookings', data={'date': '2025-11-10'})

    assert response.status_code == 302

    repo = BookingRepository(db_connection)
    all_bookings = repo.all()
    assert len(all_bookings) == 11
    newest_booking = all_bookings[-1]
    assert newest_booking.space_id == 1
    assert newest_booking.renter_id == 2
    assert str(newest_booking.date) == '2025-11-10'
    assert newest_booking.confirmed == False

def test_create_booking_for_unavailable_date_fails(db_connection, web_client):
    db_connection.seed("seeds/makersbnb.sql")

    token = jwt.encode({'user_id': 2, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
    web_client.set_cookie('jwt_token', token)

    response = web_client.post('/spaces/1/bookings', data={'date': '2025-11-25'})

    assert response.status_code == 409
    assert response.data.decode('utf-8') == "The selected date is not available for booking."

    repo = BookingRepository(db_connection)
    all_bookings = repo.all()
    assert len(all_bookings) == 10