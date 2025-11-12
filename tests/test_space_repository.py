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

        Space(1,'Cozy City Apartment', 'Modern 1-bed apartment in central London, near cafes and transport.', 120.00, 1),
        Space(2,'Seaside Cottage', 'Charming cottage overlooking the sea. Perfect for a weekend getaway.', 180.00, 2),
        Space(3,'Mountain Cabin', 'Rustic cabin with a fireplace and forest views in the Lake District.', 150.00, 3),
        Space(4,'Modern Loft', 'Bright open-plan loft in downtown Manchester with skyline views.', 200.00, 4),
        Space(5,'Countryside Retreat', 'Peaceful farmhouse surrounded by fields and trails.', 130.00, 5),
        Space(6,'Studio Flat', 'Compact studio ideal for solo travellers, near Oxford city centre.', 95.00, 6)
       
    ]


"""
When we call SpaceRepository#find
We get a single Space object reflecting the seed data.
"""

def test_get_single_space(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    space = repository.find(3)
    assert space == Space(3,'Mountain Cabin', 'Rustic cabin with a fireplace and forest views in the Lake District.', 150.00, 3)


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
        Space(1,'Cozy City Apartment', 'Modern 1-bed apartment in central London, near cafes and transport.', 120.00, 1),
        Space(2,'Seaside Cottage', 'Charming cottage overlooking the sea. Perfect for a weekend getaway.', 180.00, 2),
        Space(3,'Mountain Cabin', 'Rustic cabin with a fireplace and forest views in the Lake District.', 150.00, 3),
        Space(4,'Modern Loft', 'Bright open-plan loft in downtown Manchester with skyline views.', 200.00, 4),
        Space(5,'Countryside Retreat', 'Peaceful farmhouse surrounded by fields and trails.', 130.00, 5),
        Space(6,'Studio Flat', 'Compact studio ideal for solo travellers, near Oxford city centre.', 95.00, 6),
        Space(7, "Kent Retreat", "Breath of fresh air", 200.00, 2)
       
    ]
