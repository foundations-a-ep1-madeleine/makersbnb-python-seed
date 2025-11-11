from lib.user import User  

class UserRepository:
    def init(self, connection):  
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM users')
        users = []
        for row in rows:
            user_obj = User(row["id"], row["name"], row["email"], row["password"])
            users.append(user_obj)
        return users

    def find(self, user_id):
        rows = self._connection.execute(
            'SELECT * FROM users WHERE id = %s', [user_id])
        if not rows:
            return None
        row = rows[0]
        return User(row["id"], row["name"], row["email"], row["password"])

    def find_by_email(self, email):
        rows = self._connection.execute('SELECT * FROM users WHERE email = %s', [email])
        if not rows:
            return None
        row = rows[0]
        return User(row["id"], row["name"], row["email"], row["password"])

    def create(self, user):
        self._connection.execute(
            'INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
            [user.name, user.email, user.password]
        )
        return None

    def update(self, user):
        self._connection.execute(
            'UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s',
            [user.name, user.email, user.password, user.id]
        )
        return None

    def delete(self, user_id):
        self._connection.execute(
            'DELETE FROM users WHERE id = %s', [user_id]
        )

 