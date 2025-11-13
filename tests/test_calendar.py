from datetime import date
import json

def test_calendar_shows_available_days_and_links(db_connection, web_client):
    # Seed DB with provided data
    db_connection.seed("seeds/makersbnb.sql")

    # Request November 2025 for space 1 (seed includes availabilities for Nov/Dec)
    response = web_client.get('/spaces/1?year=2025&month=11')
    assert response.status_code == 200
    html = response.data.decode('utf-8')

    # We expect at least one available day (from seed: 2025-11-01 -> 2025-11-15)
    assert 'class="available"' in html

    # The calendar now uses checkboxes for multi-selection; ensure the form and inputs exist
    assert 'name="dates"' in html
    assert 'action="/spaces/1/book"' in html
    # ensure a known available date is present as a checkbox value
    assert 'value="2025-11-01"' in html

def test_calendar_other_months_are_shown(db_connection, web_client):
    db_connection.seed("seeds/makersbnb.sql")
    # Request December 2025 where seed includes availability for 2025-12-01..2025-12-20
    response = web_client.get('/spaces/1?year=2025&month=12')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'class="available"' in html
    assert 'name="dates"' in html
    assert 'value="2025-12-05"' in html
