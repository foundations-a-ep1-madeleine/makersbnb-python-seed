from datetime import datetime

from lib.booking import Booking
from lib.booking_repository import BookingRepository

def test_get_all_bookings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.all()

    assert bookings == [
        Booking(1, datetime(2025,11,05)),

    ]

    pass

def test_get_bookings_by_renter_id(db_connection):
    pass

def test_get_bookings_by_space_id(db_connection):
    pass