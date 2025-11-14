from lib.availability_repository import *
from lib.availability import *
from datetime import date


def test_get_all_records(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = AvailabilityRepository(db_connection)

    availability = repository.all()
   
    assert availability == [
        Availability(1,date(2025,11,1), date(2025,11,15), 1),
        Availability(2,date(2025,12,1), date(2025,12,20), 1),
        Availability(3,date(2025,11,5), date(2025,11,25), 2),
        Availability(4,date(2025,12,10), date(2025,12,31), 3),
        Availability(5,date(2025,11,15), date(2025,11,30), 4),
        Availability(6,date(2025,12,1), date(2025,12,15), 5),
        Availability(7,date(2025,11,10), date(2025,11,20), 6),
        Availability(8,date(2025, 11, 12), date(2025, 11, 19), 7),
        Availability(9,date(2025, 11, 12), date(2025, 11, 19), 8)
    ]


def test_get_single_record_by_id(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = AvailabilityRepository(db_connection)

    availability = repository.find_by_id(3)
    assert availability == Availability(3,date(2025,11,5), date(2025,11,25), 2)

   

def test_get_single_record_by_start_date(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = AvailabilityRepository(db_connection)

    availability = repository.find_by_start_date(date(2025,12,1))
    assert availability == [
    Availability(2, date(2025,12,1), date(2025,12,20), 1),
    Availability(6, date(2025,12,1), date(2025,12,15), 5)
]

def test_get_single_record_by_space_id(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = AvailabilityRepository(db_connection)

    availability = repository.find_by_space_id(5)
    assert availability ==  [Availability(6,date(2025,12,1), date(2025,12,15), 5)]



def test_create_record(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = AvailabilityRepository(db_connection)

    repository.create(Availability(None,date(2025,1,1), date(2025,10,13),6))
    availability = repository.all()
    assert availability == [
        Availability(1,date(2025,11,1), date(2025,11,15), 1),
        Availability(2,date(2025,12,1), date(2025,12,20), 1),
        Availability(3,date(2025,11,5), date(2025,11,25), 2),
        Availability(4,date(2025,12,10), date(2025,12,31), 3),
        Availability(5,date(2025,11,15), date(2025,11,30), 4),
        Availability(6,date(2025,12,1), date(2025,12,15), 5),
        Availability(7,date(2025,11,10), date(2025,11,20), 6),
        Availability(8,date(2025, 11, 12), date(2025, 11, 19), 7),
        Availability(9,date(2025, 11, 12), date(2025, 11, 19), 8),
        Availability(10,date(2025,1,1), date(2025,10,13), 6)
    ]

def test_update_record(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = AvailabilityRepository(db_connection)

    repository.update(Availability(2,date(2025,1,1), date(2025,10,13),6))
    availability = repository.all()
    assert availability == [
        Availability(1,date(2025,11,1), date(2025,11,15), 1),
        Availability(2,date(2025,1,1), date(2025,10,13),6),
        Availability(3,date(2025,11,5), date(2025,11,25), 2),
        Availability(4,date(2025,12,10), date(2025,12,31), 3),
        Availability(5,date(2025,11,15), date(2025,11,30), 4),
        Availability(6,date(2025,12,1), date(2025,12,15), 5),
        Availability(7,date(2025,11,10), date(2025,11,20), 6),
        Availability(8,date(2025, 11, 12), date(2025, 11, 19), 7),
        Availability(9,date(2025, 11, 12), date(2025, 11, 19), 8)
    ]


def test_delete_record(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = AvailabilityRepository(db_connection)

    repository.delete(2)
    availability = repository.all()
    assert availability == [
        Availability(1,date(2025,11,1), date(2025,11,15), 1),
        Availability(3,date(2025,11,5), date(2025,11,25), 2),
        Availability(4,date(2025,12,10), date(2025,12,31), 3),
        Availability(5,date(2025,11,15), date(2025,11,30), 4),
        Availability(6,date(2025,12,1), date(2025,12,15), 5),
        Availability(7,date(2025,11,10), date(2025,11,20), 6),
        Availability(8,date(2025, 11, 12), date(2025, 11, 19), 7),
        Availability(9,date(2025, 11, 12), date(2025, 11, 19), 8)
    ]



