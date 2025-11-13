from lib.space_repository import *
from lib.space import *

"""
When we call SpaceRepository#all
We get a list of Space objects reflecting the seed data.
"""
def test_get_all_spaces(db_connection): 
    db_connection.seed("seeds/makersbnb.sql") 
    repository = SpaceRepository(db_connection) 

    spaces = repository.all() 

    assert spaces == [

        Space(1,'Cozy City Apartment', 'Modern 1-bed apartment in central London, near cafes and transport.', 120.00, 1, 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop'),
        Space(2,'Seaside Cottage', 'Charming cottage overlooking the sea. Perfect for a weekend getaway.', 180.00, 2, 'https://images.unsplash.com/photo-1499696010180-025ef6e1a8f9?w=800&h=600&fit=crop'),
        Space(3,'Mountain Cabin', 'Rustic cabin with a fireplace and forest views in the Lake District.', 150.00, 3, 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop'),
        Space(4,'Modern Loft', 'Bright open-plan loft in downtown Manchester with skyline views.', 200.00, 4, 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&h=600&fit=crop'),
        Space(5,'Countryside Retreat', 'Peaceful farmhouse surrounded by fields and trails.', 130.00, 5, 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&h=600&fit=crop'),
        Space(6,'Studio Flat', 'Compact studio ideal for solo travellers, near Oxford city centre.', 95.00, 6, 'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&h=600&fit=crop')
       
    ]

"""
When we call SpaceRepository#find_by_user
We get a list of Space objects owned by a given user_id, reflecting the seed data.
"""
def test_get_all_spaces(db_connection): 
    db_connection.seed("seeds/makersbnb.sql") 
    repository = SpaceRepository(db_connection) 

    spaces = repository.find_by_user(1) 

    assert spaces == [
        Space(1,'Cozy City Apartment', 'Modern 1-bed apartment in central London, near cafes and transport.', 120.00, 1, 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop'),
    ]


"""
When we call SpaceRepository#find
We get a single Space object reflecting the seed data.
"""

def test_get_single_space(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    space = repository.find(3)
    assert space == Space(3,'Mountain Cabin', 'Rustic cabin with a fireplace and forest views in the Lake District.', 150.00, 3, 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop')


"""
When we call SpaceRepository#create
We get a new space in the database.
"""

def test_create_space(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    repository.create(Space(None, "Kent Retreat", "Breath of fresh air", 200.00, 2))

    result = repository.all()
    assert result == [
        Space(1,'Cozy City Apartment', 'Modern 1-bed apartment in central London, near cafes and transport.', 120.00, 1, 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop'),
        Space(2,'Seaside Cottage', 'Charming cottage overlooking the sea. Perfect for a weekend getaway.', 180.00, 2, 'https://images.unsplash.com/photo-1499696010180-025ef6e1a8f9?w=800&h=600&fit=crop'),
        Space(3,'Mountain Cabin', 'Rustic cabin with a fireplace and forest views in the Lake District.', 150.00, 3, 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop'),
        Space(4,'Modern Loft', 'Bright open-plan loft in downtown Manchester with skyline views.', 200.00, 4, 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&h=600&fit=crop'),
        Space(5,'Countryside Retreat', 'Peaceful farmhouse surrounded by fields and trails.', 130.00, 5, 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&h=600&fit=crop'),
        Space(6,'Studio Flat', 'Compact studio ideal for solo travellers, near Oxford city centre.', 95.00, 6, 'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&h=600&fit=crop'),
        Space(7, "Kent Retreat", "Breath of fresh air", 200.00, 2, None)
       
    ]
