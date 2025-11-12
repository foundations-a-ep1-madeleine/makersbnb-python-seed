from playwright.sync_api import Page, expect
import re
from datetime import date
import json

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



"""
We can render the index page
"""
def test_get_index(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/index")

    # We look for the header
    header = page.locator(".homepage-header h1")

    # We assert that it has the updated heading text
    expect(header).to_have_text("Find Your Perfect Space")
    
    # We check that space cards are rendered
    space_cards = page.locator(".space-card")
    expect(space_cards).to_have_count(6)


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
    assert response.data.decode("utf-8") == "\n".join([
        "Availability (3, 2025-11-05, 2025-11-25, 2)",
        "Availability (8, 2025-05-27, 2025-05-29, 2)"
    ])


def test_book_button_navigates_to_availability(page, test_web_address, db_connection):
    # Arrange
    db_connection.seed("seeds/makersbnb.sql")

    # Go to spaces list and open first space
    page.goto(f"http://{test_web_address}/spaces")
    first_card = page.locator('.space-card-link').first
    first_card.click()

    # Assert the Book button is present on the detail page
    book_button = page.locator('a.view-button', has_text="Book").first
    expect(book_button).to_be_visible()

    # Click the Book button and verify navigation to availability endpoint
    book_button.click()

    expect(page).to_have_url(re.compile(rf"^http://{re.escape(test_web_address)}/spaces/1/availability\??$"))
    # The availability endpoint returns plain text with availability entries
    expect(page.locator('body')).to_contain_text("Availability (1, 2025-11-01, 2025-11-15, 1)")