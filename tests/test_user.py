from lib.user import User

def test_user_constructs():
    user = User(1, "Test Name", "test@email.com", "password123")
    assert user.id == 1
    assert user.name == "Test Name"
    assert user.email == "test@email.com"
    assert user.password == "password123"

def test_users_are_equal():
    user1 = User(1, "Test Name", "test@email.com", "password123")
    user2 = User(1, "Test Name", "test@email.com", "password123")
    assert user1 == user2

def test_user_formats_to_string():
    user = User(1, "Test Name", "test@email.com", "password123")
    assert str(user) == "User(1, Test Name, test@email.com, password123)"