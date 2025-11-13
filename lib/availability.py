from datetime import date

class Availability:
    def __init__(self, id, start_date, end_date, space_id):
        self.id = id

        # if isinstance(start_date, str):
        #     self.start_date = date.fromisoformat(start_date)
        # else:
        #     self.start_date = start_date

        # if isinstance(end_date, str):
        #     self.end_date = date.fromisoformat(end_date)
        # else:
        #     self.end_date = end_date
        
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.space_id = space_id

    def to_dict(self):
        return {
            "id": self.id,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "space_id": self.space_id
        }

    def __eq__(self, other):
        if not isinstance(other, Availability):
            return False
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return (
            f"Availability ({self.id}, {self.start_date}, {self.end_date}, {self.space_id})"
        )
