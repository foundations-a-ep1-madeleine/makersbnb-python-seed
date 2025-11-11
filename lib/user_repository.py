from lib.user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM users')
        users = []
        for row in rows:
            user = User(row["id"], row["name"], row["email"], row["password_hash"], row["created_at"])
            users.append(user)
        return users

    def find(self, user_id):
        rows = self._connection.execute('SELECT * FROM users WHERE id = %s', [user_id])
        if not rows: return None
        row = rows[0]
        return User(row["id"], row["name"], row["email"], row["password_hash"], row["created_at"])

    def find_by_email(self, email):
        rows = self._connection.execute('SELECT * FROM users WHERE email = %s', [email])
        if not rows: return None
        row = rows[0]
        return User(row["id"], row["name"], row["email"], row["password_hash"], row["created_at"])

    def create(self, user):
        self._connection.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)',
            [user.name, user.email, user.password_hash]
        )
        return None

    def delete(self, user_id):
        self._connection.execute('DELETE FROM users WHERE id = %s', [user_id])
        return None

