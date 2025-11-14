from lib.user_repository import UserRepository
from lib.user import User
from datetime import datetime

def test_get_all_users(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    users = repository.all()

   
    assert len(users) == 7

    assert users[0].name == 'Isaac Madgewick'
    assert users[0].email == 'isaacm@example.com'
    assert users[0].password_hash == 'hash_for_isaac'
    assert isinstance(users[0].created_at, datetime)

    assert users[5].name == 'Margot Bourne'
    assert users[5].email == 'margotb@example.com'
    assert users[5].password_hash == 'hash_for_margot'

def test_find_user_by_id(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    user = repository.find(2) 
    assert user.name == 'Sabia Jeyaratnam'
    assert user.email == 'sabiaj@example.com'

def test_create_user(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)

    new_user = User(None, "Test User", "test@example.com", "test_hash")
    repository.create(new_user)

    all_users = repository.all()
   
    assert len(all_users) == 8
    assert all_users[-1].name == "Test User"

def test_delete_user(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = UserRepository(db_connection)
    repository.delete(1) 

    all_users = repository.all()
    
    assert len(all_users) == 6
    
    assert all_users[0].name == 'Sabia Jeyaratnam'