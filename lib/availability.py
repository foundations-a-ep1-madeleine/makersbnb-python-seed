
from datetime import date

class Availability:
    def init(self, id, start_date, end_date, space_id):
        self.id = id

        if isinstance(start_date, str):
            self.start_date = date.fromisoformat(start_date)
        else:
            self.start_date = start_date

        if isinstance(end_date, str):
            self.end_date = date.fromisoformat(end_date)
        else:
            self.end_date = end_date

        self.space_id = space_id 

    def eq(self, other):
        return self.dict == other.dict

    def repr(self):
        return f"Availability({self.id}, {self.start_date}, {self.end_date}, {self.space_id})"
