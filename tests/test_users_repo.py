from lib.user_repository import UserRepository
from lib.user import User

def test_get_all_users(db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql") 
    repository = UserRepository(db_connection)
    users = repository.all()
    assert users == [
        User(1, "Nazar", "nazar@test.com", "password123"),
        User(2, "Margo", "margo@test.com", "password456")
    ]

def test_find_user_by_id(db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    repository = UserRepository(db_connection)
    user = repository.find(1)
    assert user == User(1, "Nazar", "nazar@test.com", "password123")

def test_find_user_by_email(db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    repository = UserRepository(db_connection)
    user = repository.find_by_email("margo@test.com")
    assert user == User(2, "Margo", "margo@test.com", "password456")

def test_create_user(db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    repository = UserRepository(db_connection)
    new_user = User(None, "Sam", "sam@test.com", "newpass")
    repository.create(new_user)
    all_users = repository.all()
    assert all_users == [
        User(1, "Nazar", "nazar@test.com", "password123"),
        User(2, "Margo", "margo@test.com", "password456"),
        User(3, "Sam", "sam@test.com", "newpass")
    ]

def test_update_user(db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    repository = UserRepository(db_connection)
    user_to_update = repository.find(1)
    user_to_update.name = "Nazarii"
    repository.update(user_to_update)
    updated_user = repository.find(1)
    assert updated_user == User(1, "Nazarii", "nazar@test.com", "password123")

def test_delete_user(db_connection):
    db_connection.seed("seeds/makersbnb_seed.sql")
    repository = UserRepository(db_connection)
    repository.delete(1)
    all_users = repository.all()
    assert all_users == [
        User(2, "Margo", "margo@test.com", "password456")
    ]
