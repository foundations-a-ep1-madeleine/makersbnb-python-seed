from lib.booking import Booking

class BookingRepository:

    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        bookings = self._connection.execute('SELECT * from bookings')
        booking_list = []
        for booking in bookings:
            booking_list.append(Booking(booking["id"], booking["date"], booking["confirmed"], booking["space_id"], booking["user_id"]))
        return booking_list
    
    # Returns a single booking by its UID
    def get_by_id(self, id):
        bookings = self._connection.execute('SELECT * from bookings WHERE id = %s', [id])
        booking = bookings[0]
        return Booking(booking["id"], booking["date"], booking["confirmed"], booking["space_id"], booking["user_id"])
    
    # Returns a list of bookings when given a renter id (user id which rented)
    def get_by_renter(self, renter_id):
        bookings = self._connection.execute('SELECT * from bookings WHERE user_id = %s', [renter_id])
        booking_list = []
        for booking in bookings:
            booking_list.append(Booking(booking["id"], booking["date"], booking["confirmed"], booking["space_id"], booking["user_id"]))
        return booking_list
    
    # Returns a list of bookings when given a space id
    def get_by_space(self, space_id):
        bookings = self._connection.execute('SELECT * from bookings WHERE space_id = %s', [space_id])
        booking_list = []
        for booking in bookings:
            booking_list.append(Booking(booking["id"], booking["date"], booking["confirmed"], booking["space_id"], booking["user_id"]))
        return booking_list
    
    # Creates a new booking
    def create(self, booking):
        self._connection.execute('INSERT INTO bookings (date, confirmed, space_id, user_id) VALUES (%s, %s, %s, %s)', [
                                 booking.date, booking.confirmed, booking.space_id, booking.renter_id])
        return None

    # Deletes a booking by id
    def delete(self, id):
        self._connection.execute(
            'DELETE FROM bookings WHERE id = %s', [id])
        return None