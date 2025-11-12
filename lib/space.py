class Space:
    
    def __init__(self, id, name, description, price, user_id, image_url=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.user_id = user_id
        self.image_url = image_url

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Space({self.id}, {self.name}, {self.description}, {self.price}, {self.user_id}, {self.image_url})"
