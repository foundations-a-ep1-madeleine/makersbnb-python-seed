from lib.booking import Booking
from datetime import datetime

def test_booking_init():
    now = datetime.now()
    booking = Booking(1, now, False, 0, 0)
    assert booking.id == 1
    assert booking.date == now
    assert booking.confirmed == False
    assert booking.space_id == 0
    assert booking.renter_id == 0 #user id

def test_booking_compare_equal():
    now = datetime.now()
    booking1 = Booking(1, now, False, 0, 0)
    booking2 = Booking(1, now, False, 0, 0)

    assert booking1 == booking2

def test_booking_compare_unequal():
    now = datetime.now()
    booking1 = Booking(3, now, True, 2, 10)
    booking2 = Booking(1, now, False, 0, 0)

    assert booking1 != booking2

def test_booking_format():
    now = datetime.now()
    booking = Booking(1, now, False, 0, 0)

    assert str(booking) == f"Booking(1, {now}, False, 0, 0)"