from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection
from lib.availability_repository import AvailabilityRepository
from lib.space_repository import SpaceRepository
from lib.availability import Availability
from lib.space import Space
from datetime import date

"""
Tests for date filtering on spaces listing page
"""

def test_spaces_page_shows_all_spaces_without_date_filter(page, test_web_address, db_connection):
    # Seed database
    db_connection.seed("seeds/makersbnb.sql")
    
    page.goto(f"http://{test_web_address}/spaces")
    
    # Should show all spaces when no dates are provided
    space_cards = page.locator(".space-card-link")
    expect(space_cards).to_have_count(8)  # 6 spaces in seed data


def test_spaces_page_filters_by_date_range(page, test_web_address, db_connection):
    # Seed database already has availabilities, so we check existing ones:
    # Space 1 (Cozy City Apartment): Nov 1-15, 2025
    # Space 2 (Seaside Cottage): Nov 5-25, 2025
    # Space 4 (Modern Loft): Nov 15-30, 2025
    # Space 6 (Studio Flat): Nov 10-20, 2025
    db_connection.seed("seeds/makersbnb.sql")
    
    # Navigate to spaces page
    page.goto(f"http://{test_web_address}/spaces")
    
    # Fill in date filter: Nov 12-14, 2025
    # Space 1: available (Nov 1-15 includes 12-14)
    # Space 2: available (Nov 5-25 includes 12-14)
    # Space 4: NOT available (Nov 15-30 doesn't include 12-14)
    # Space 6: available (Nov 10-20 includes 12-14)
    page.fill("#start_date", "2025-11-12")
    page.fill("#end_date", "2025-11-14")
    page.click(".filter-button")
    
    # Should show spaces 1, 2, and 6
    space_cards = page.locator(".space-card-link")
    expect(space_cards).to_have_count(5)
    
    # Verify the filtered spaces contain expected text
    page_content = page.content()
    assert "Cozy City Apartment" in page_content  # Space 1
    assert "Seaside Cottage" in page_content  # Space 2
    assert "Studio Flat" in page_content  # Space 6


def test_spaces_page_shows_no_results_when_no_spaces_available(page, test_web_address, db_connection):
    # Seed database
    # Seed has availabilities but none that cover Feb 1-5, 2026
    db_connection.seed("seeds/makersbnb.sql")
    
    page.goto(f"http://{test_web_address}/spaces")
    
    # Search for dates outside all availability ranges
    page.fill("#start_date", "2026-02-01")
    page.fill("#end_date", "2026-02-05")
    page.click(".filter-button")
    
    # Should show no spaces
    space_cards = page.locator(".space-card-link")
    expect(space_cards).to_have_count(0)


def test_spaces_page_preserves_date_inputs_after_filtering(page, test_web_address, db_connection):
    # Seed database
    db_connection.seed("seeds/makersbnb.sql")
    
    page.goto(f"http://{test_web_address}/spaces")
    
    # Fill in dates and submit
    page.fill("#start_date", "2025-11-12")
    page.fill("#end_date", "2025-11-14")
    page.click(".filter-button")
    
    # Verify inputs retain the values
    start_input = page.locator("#start_date")
    end_input = page.locator("#end_date")
    
    expect(start_input).to_have_value("2025-11-12")
    expect(end_input).to_have_value("2025-11-14")


def test_spaces_page_shows_clear_button_when_dates_provided(page, test_web_address, db_connection):
    # Seed database
    db_connection.seed("seeds/makersbnb.sql")
    
    page.goto(f"http://{test_web_address}/spaces")
    
    # Clear button should not be visible initially
    clear_button = page.locator(".clear-filter")
    expect(clear_button).to_have_count(0)
    
    # Fill in dates and submit
    page.fill("#start_date", "2025-11-12")
    page.fill("#end_date", "2025-11-14")
    page.click(".filter-button")
    
    # Clear button should now be visible
    expect(clear_button).to_be_visible()
    
    # Click clear button
    clear_button.click()
    
    # Should redirect to spaces page without dates
    expect(page).to_have_url(f"http://{test_web_address}/spaces")
    
    # Inputs should be empty
    expect(page.locator("#start_date")).to_have_value("")
    expect(page.locator("#end_date")).to_have_value("")


def test_spaces_page_requires_both_dates_for_filtering(page, test_web_address, db_connection):
    # Seed database
    db_connection.seed("seeds/makersbnb.sql")
    
    page.goto(f"http://{test_web_address}/spaces")
    
    # Fill only start date
    page.fill("#start_date", "2025-11-12")
    page.click(".filter-button")
    
    # Should show all spaces (no filtering)
    space_cards = page.locator(".space-card-link")
    expect(space_cards).to_have_count(8)
    
    # Reset and fill only end date
    page.goto(f"http://{test_web_address}/spaces")
    page.fill("#end_date", "2025-11-14")
    page.click(".filter-button")
    
    # Should show all spaces (no filtering)
    expect(space_cards).to_have_count(8)


def test_spaces_page_handles_partial_availability_correctly(page, test_web_address, db_connection):
    # Seed database
    # From seeds: Space 1 has Nov 1-15 and Dec 1-20
    db_connection.seed("seeds/makersbnb.sql")
    
    page.goto(f"http://{test_web_address}/spaces")
    
    # Search for Nov 14 - Dec 3 (crosses the gap between Nov 15 and Dec 1)
    # Space 1 covers Nov 14-15 but NOT Nov 16-30, so it should NOT appear
    page.fill("#start_date", "2025-11-14")
    page.fill("#end_date", "2025-12-03")
    page.click(".filter-button")
    
    # Space 1 should NOT appear because Nov 16-30 are not available (gap in availability)
    space_cards = page.locator(".space-card-link")
    expect(space_cards).to_have_count(0)


def test_spaces_page_handles_multiple_availability_ranges(page, test_web_address, db_connection):
    # Seed database already has space 1 with Nov 1-15 and Dec 1-20
    # This tests that a space with multiple availability ranges works correctly
    db_connection.seed("seeds/makersbnb.sql")
    
    page.goto(f"http://{test_web_address}/spaces")
    
    # Search within first range (Nov 1-15)
    page.fill("#start_date", "2025-11-02")
    page.fill("#end_date", "2025-11-04")
    page.click(".filter-button")
    
    space_cards = page.locator(".space-card-link")
    # Space 1 should appear (and possibly others)
    page_content = page.content()
    assert "Cozy City Apartment" in page_content
    
    # Search across gap (Nov 16 - Nov 30 not available for space 1)
    page.goto(f"http://{test_web_address}/spaces")
    page.fill("#start_date", "2025-11-16")
    page.fill("#end_date", "2025-11-30")
    page.click(".filter-button")
    
    # Space 1 should NOT appear because it has a gap from Nov 16-30
    page_content = page.content()
    assert "Cozy City Apartment" not in page_content
    
    # Search within second range (Dec 1-20)
    page.goto(f"http://{test_web_address}/spaces")
    page.fill("#start_date", "2025-12-05")
    page.fill("#end_date", "2025-12-10")
    page.click(".filter-button")
    
    # Space 1 should appear again
    page_content = page.content()
    assert "Cozy City Apartment" in page_content
