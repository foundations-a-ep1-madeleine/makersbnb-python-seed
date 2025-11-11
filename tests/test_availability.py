
from lib.availability import *
from datetime import datetime


def test_availability_constructors():
    start_date = datetime(2025,1,1)
    end_date = datetime(2026,1,1)
    availability = Availability(1,start_date.strftime("%x"), end_date.strftime("%x"),1)
    assert availability.id == 1 
    assert availability.start_date == "01/01/25"
    assert availability.end_date == "01/01/26"
    assert availability.space_id == 1

def test_availability_are_equal():
    start_date = datetime(2025,1,1)
    end_date = datetime(2026,1,1)
    availability1 = Availability(1,start_date.strftime("%x"), end_date.strftime("%x"),1)
    availability2 = Availability(1,start_date.strftime("%x"), end_date.strftime("%x"),1)
    assert availability1 == availability2

def test_availability_format():
    start_date = datetime(2025,1,1)
    end_date = datetime(2026,1,1)
    availability = Availability(1,start_date.strftime("%x"), end_date.strftime("%x"),1)
    assert str(availability) == "Availability (1, 01/01/25, 01/01/26, 1)"