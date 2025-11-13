from playwright.sync_api import Page, expect
import re
from datetime import date
import json

from lib.user_repository import UserRepository # for signup testing
import bcrypt #for signup hash checking

def test_get_spaces(page, test_web_address, db_connection): 
    db_connection.seed("seeds/makersbnb.sql")

    page.goto(f"http://{test_web_address}/spaces")

    # Check that space cards are rendered in the grid
    space_cards = page.locator(".space-card")
    expect(space_cards).to_have_count(6)
    
    # Check that the first space has the correct name
    first_space_name = page.locator(".space-name").first
    expect(first_space_name).to_contain_text("Cozy City Apartment")

    # clicking the first card navigates to its detail page
    first_card = page.locator('.space-card-link').first
    first_card.click()
    # expect to arrive on the single-space page and see the space name
    # allow an optional trailing query marker added by the test runner
    expect(page).to_have_url(re.compile(rf"^http://{re.escape(test_web_address)}/spaces/1\??$"))
    expect(page.locator('.space-name')).to_contain_text('Cozy City Apartment')



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
    # assert response.data.decode("utf-8") == "\n".join([
    #     "Availability (3, 2025-11-05, 2025-11-25, 2)",
    #     "Availability (8, 2025-05-27, 2025-05-29, 2)"
    # ])

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
        },
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
