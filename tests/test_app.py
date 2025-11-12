from playwright.sync_api import Page, expect
from datetime import date
import json

from lib.user_repository import UserRepository # for signup testing
import bcrypt #for signup hash checking

def test_get_spaces(page, test_web_address, db_connection): 
    db_connection.seed("seeds/makersbnb.sql")
   
    page.goto(f"http://{test_web_address}/spaces")

    div_tags = page.locator("div")
    expect(div_tags).to_have_text([

        "Name: Cozy City Apartment\nDescription: Modern 1-bed apartment in central London, near cafes and transport.\nPrice: 120.00\nUser_id: 1",
        "Name: Seaside Cottage\nDescription: Charming cottage overlooking the sea. Perfect for a weekend getaway.\nPrice: 180.00\nUser_id: 2",
        "Name: Mountain Cabin\nDescription: Rustic cabin with a fireplace and forest views in the Lake District.\nPrice: 150.00\nUser_id: 3",
        "Name: Modern Loft\nDescription: Bright open-plan loft in downtown Manchester with skyline views.\nPrice: 200.00\nUser_id: 4",
        "Name: Countryside Retreat\nDescription: Peaceful farmhouse surrounded by fields and trails.\nPrice: 130.00\nUser_id: 5",
        "Name: Studio Flat\nDescription: Compact studio ideal for solo travellers, near Oxford city centre.\nPrice: 95.00\nUser_id: 6"
    ])



"""
We can render the index page
"""
def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/index")

    # We look at the <p> tag
    p_tag = page.locator("p")

    # We assert that it has the text "This is the homepage."
    expect(p_tag).to_have_text("This is the homepage.")


def test_get_space_availability(db_connection, web_client):
    db_connection.seed("seeds/makersbnb.sql")

    response = web_client.get("/spaces/1/availability")

    assert response.status_code == 200

    expected_json = [
        {
            "id": 1,
            "start_date": "2025-11-01",
            "end_date": "2025-11-15",
            "space_id": 1,
        },
        {
            "id": 2,
            "start_date": "2025-12-01",
            "end_date": "2025-12-20",
            "space_id": 1,
        }
    ]

    json_string = response.data.decode("utf-8")
    actual_data = json.loads(json_string)
    assert actual_data == expected_json

def test_post_space_availability(db_connection, web_client):
    db_connection.seed("seeds/makersbnb.sql")

    response = web_client.post("/spaces/availability", data={
        "start_date": date(2025,5,27),
        "end_date": date(2025, 5, 29),
        "space_id": 2,
    })

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Availability added"

    response = web_client.get("/spaces/2/availability")

    assert response.status_code == 200

    expected_json = [
        {
            "id": 3,
            "start_date": "2025-11-05",
            "end_date": "2025-11-25",
            "space_id": 2,
        },
        {
            "id": 8,
            "start_date": "2025-05-27",
            "end_date": "2025-05-29",
            "space_id": 2,
        }
    ]

    json_string = response.data.decode("utf-8")
    actual_data = json.loads(json_string)
    assert actual_data == expected_json

def test_signup_backend_correct(db_connection, web_client):
    db_connection.seed("seeds/makersbnb.sql")

    response = web_client.post("/signup", data={
        'name': "John Smith",
        'email': "johns@xyz123.com",
        "password": "reallygoodpassword123!",
    })

    assert response.status_code == 201

    repo = UserRepository(db_connection)
    user = repo.find(7)

    assert user.name == "John Smith" and user.email == "johns@xyz123.com"
    assert bcrypt.checkpw("reallygoodpassword123!".encode('utf-8'), user.password_hash.encode("utf-8")) == True

def test_signup_backend_incorrect(db_connection, web_client):
    db_connection.seed("seeds/makersbnb.sql")

    response = web_client.post("/signup", data={
        'name': "John Smith",
        'email': "johns@xyz123.com",
        "password": "reallygoodpassword123!",
    })

    assert response.status_code == 201

    repo = UserRepository(db_connection)
    user = repo.find(7)

    assert user.name == "John Smith" and user.email == "johns@xyz123.com"
    assert bcrypt.checkpw("nottheactualpasswordwhat".encode('utf-8'), user.password_hash.encode("utf-8")) == False