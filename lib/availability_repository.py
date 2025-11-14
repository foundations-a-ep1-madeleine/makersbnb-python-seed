from lib.availability import *
from datetime import date 
class AvailabilityRepository():
    
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM availabilities ORDER BY id')
        availabilities = []
        for row in rows:
            item = Availability(row["id"],row["start_date"],row["end_date"],row["space_id"])
            availabilities.append(item)
        return availabilities


    def find_by_id(self,id):
        rows = self._connection.execute('SELECT * FROM availabilities WHERE id = %s ', [id])
        row = rows[0]
        availability = Availability(row["id"],row["start_date"],row["end_date"],row["space_id"])
        return availability

    
    def find_by_start_date(self,start_date):
        rows = self._connection.execute('SELECT * FROM availabilities WHERE start_date = %s ', [start_date])
        availabilities = []
        for row in rows:
            item = Availability(row["id"],row["start_date"],row["end_date"],row["space_id"])
            availabilities.append(item)
        return availabilities
    

    def find_by_space_id(self,space_id):
        rows = self._connection.execute('SELECT * FROM availabilities WHERE space_id = %s ', [space_id])
        availabilities = []
        for row in rows:
            item = Availability(row["id"],row["start_date"],row["end_date"],row["space_id"])
            availabilities.append(item)
        
        return availabilities

    def create(self,availability):
        self._connection.execute('INSERT INTO availabilities(start_date,end_date, space_id) VALUES(%s,%s,%s)',[availability.start_date, availability.end_date, availability.space_id])
        return None

    def update(self,availability):
        self._connection.execute('UPDATE availabilities SET start_date = %s, end_date = %s , space_id = %s WHERE id = %s',[availability.start_date, availability.end_date, availability.space_id, availability.id])
        return None

    def delete(self,id):
        self._connection.execute('DELETE FROM availabilities WHERE id = %s',[id])
        return None

    def is_date_available(self, space_id, booking_date):
        if isinstance(booking_date, str):
            booking_date = date.fromisoformat(booking_date)

        available_periods = self.find_by_space_id(space_id)

        for period in available_periods:
            if period.start_date <= booking_date <= period.end_date:
                return True

        return False