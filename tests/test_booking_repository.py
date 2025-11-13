from datetime import date

from lib.booking import Booking
from lib.booking_repository import BookingRepository

def test_get_all_bookings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.all()

    assert bookings == [
        Booking(1, date(2025,11,5), False, 1, 2),
        Booking(2, date(2025,11,10), False, 2, 3),
        Booking(3, date(2025,12,12), True, 3, 4),
        Booking(4, date(2025,11,18), True, 4, 5),
        Booking(5, date(2025,12,5), False, 5, 6),
        Booking(6, date(2025,11,12), True, 6, 1),
    ]

    pass

def test_get_booking(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    booking = repository.get_by_id(2)

    assert booking == Booking(2, date(2025,11,10), False, 2, 3)

def test_get_bookings_by_renter_id(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    booking = repository.get_by_renter(4)

    assert booking == [Booking(3, date(2025,12,12), True, 3, 4)]

def test_get_bookings_by_space_id(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    booking = repository.get_by_space(4)

    assert booking == [Booking(4, date(2025,11,18), True, 4, 5)]

def test_create_booking(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    repository.create(Booking(None, date(2025,5,5), True, 2, 2))

    booking = repository.get_by_id(7)
    assert booking == Booking(7, date(2025,5,5), True, 2, 2)

def test_delete_booking(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    repository.delete(1)

    bookings = repository.all()
    assert bookings == [
        Booking(2, date(2025,11,10), False, 2, 3),
        Booking(3, date(2025,12,12), True, 3, 4),
        Booking(4, date(2025,11,18), True, 4, 5),
        Booking(5, date(2025,12,5), False, 5, 6),
        Booking(6, date(2025,11,12), True, 6, 1),
    ]


def test_get_by_host_id(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)
    bookings = repository.get_by_host(3)
    assert bookings == [{'confirmed': True,'space_id': 3, 'date': date(2025, 12, 12), 'host_name': 'Sam Llewellyn', 'space_name': 'Mountain Cabin'}]

