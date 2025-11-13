from lib.availability import Availability
from lib.availability_repository import AvailabilityRepository
from datetime import date

def test_create_does_not_add_overlapping_availability(db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    repository = AvailabilityRepository(db_connection)

    overlapping_period_1 = Availability(None, date(2025, 11, 5), date(2025, 11, 10), 1)
    result1 = repository.create(overlapping_period_1)
    assert result1 == False

    overlapping_period_2 = Availability(None, date(2025, 10, 25), date(2025, 11, 5), 1)
    result2 = repository.create(overlapping_period_2)
    assert result2 == False

    overlapping_period_3 = Availability(None, date(2025, 11, 10), date(2025, 11, 20), 1)
    result3 = repository.create(overlapping_period_3)
    assert result3 == False

    overlapping_period_4 = Availability(None, date(2025, 10, 20), date(2025, 11, 20), 1)
    result4 = repository.create(overlapping_period_4)
    assert result4 == False

    non_overlapping_period = Availability(None, date(2025, 10, 1), date(2025, 10, 15), 1)
    result5 = repository.create(non_overlapping_period)
    assert result5 == True

    all_availabilities_for_space_1 = repository.find_by_space_id(1)
    assert len(all_availabilities_for_space_1) == 3


 