class Booking:

    def __init__(self, id, date, confirmed, space_id, renter_id):
        self.id = id
        self.date = date
        self.confirmed = confirmed
        self.space_id = space_id
        self.renter_id = renter_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Booking({self.id}, {self.date}, {self.confirmed}, {self.space_id}, {self.renter_id})"