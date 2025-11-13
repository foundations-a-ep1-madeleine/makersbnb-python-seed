from lib.space import *

class SpaceRepository:

    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from spaces')
        spaces = []
        for row in rows:
            item = Space(row["id"], row["name"], row["description"], row["price"], row["user_id"], row["image_url"])
            spaces.append(item)
        return spaces

    def find_by_user(self, user_id):
        rows = self._connection.execute('SELECT * from spaces WHERE user_id = %s', [user_id])
        spaces = []
        for row in rows:
            item = Space(row["id"], row["name"], row["description"], row["price"], row["user_id"], row["image_url"])
            spaces.append(item)
        return spaces

    def find(self, space_id):
        rows = self._connection.execute(
            'SELECT * from spaces WHERE id = %s', [space_id])
        row = rows[0]
        return Space(row["id"], row["name"], row["description"], row["price"], row["user_id"], row["image_url"])
    
    def create(self, space):
        self._connection.execute('INSERT INTO spaces (name, description, price, user_id) VALUES (%s, %s, %s, %s)', [
                                 space.name, space.description, space.price, space.user_id ])
        return None

    def delete(self, space_id):
        self._connection.execute(
            'DELETE FROM spaces WHERE id = %s', [space_id])
        return None
