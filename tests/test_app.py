from playwright.sync_api import Page, expect

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