from lib.space import *

"""
space constucts with id, name, description, price, user_id.
"""
def test_space_constructs():
    space = Space(1, "Test Name", "Test Description", "Test Price", "Test User ID")
    assert space.id == 1
    assert space.name == "Test Name"
    assert space.description == "Test Description"
    assert space.price == "Test Price"
    assert space.user_id == "Test User ID"

"""
We can format spaces to strings nicely
"""
def test_spaces_format_nicely():
    space = Space(1, "Test Name", "Test Description", "Test Price", "Test User ID")
    assert str(space) == "Space(1, Test Name, Test Description, Test Price, Test User ID)"
    

"""
We can compare two identical spaces
And have them be equal
"""
def test_spaces_are_equal():
    space1 = Space(1, "Test Name", "Test Description", "Test Price", "Test User ID")
    space2 = Space(1, "Test Name", "Test Description", "Test Price", "Test User ID")
    assert space1 == space2
   