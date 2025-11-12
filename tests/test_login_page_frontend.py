from playwright.sync_api import Page, expect


def test_page_title_and_main_heading(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")

    expect(page).to_have_title("Makersbnb")

    logo_text = page.locator(".logo p")
    expect(logo_text).to_have_text("makersbnb")

    main_heading = page.get_by_role("heading", name="Welcome Home")
    expect(main_heading).to_be_visible()


def test_navigation_links(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")

    sign_up_link = page.get_by_role("link", name="Sign Up")
    expect(sign_up_link).to_be_visible()
    expect(sign_up_link).to_have_attribute("href", "/signup")

    about_link = page.get_by_role("link", name="About")
    expect(about_link).to_be_visible()
    expect(about_link).to_have_attribute("href", "/about")


def test_login_form_elements(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")

    expect(page.get_by_role("heading", name="Login")).to_be_visible()

    email_input = page.get_by_label("Email Address")
    expect(email_input).to_be_visible()
    expect(email_input).to_have_attribute("name", "email")

    password_input = page.get_by_label("Password")
    expect(password_input).to_be_visible()
    expect(password_input).to_have_attribute("name", "password")

    login_button = page.get_by_role("button", name="Log In")
    expect(login_button).to_be_visible()
    expect(login_button).to_have_attribute("type", "submit")


def test_can_fill_and_submit_form(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")

    test_email = "test@example.com"
    test_password = "securepassword123"

    page.get_by_label("Email Address").fill(test_email)
    page.get_by_label("Password").fill(test_password)

    expect(page.get_by_label("Email Address")).to_have_value(test_email)
    expect(page.get_by_label("Password")).to_have_value(test_password)

    login_form = page.locator("form.login-form")
    expect(login_form).to_have_attribute("action", "/submit-login")
    expect(login_form).to_have_attribute("method", "POST")


def test_footer_contains_copyright(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")

    footer = page.locator(".footer")
    expect(footer).to_be_visible()

    copyright_text = footer.get_by_text("©2025 Makers Academy")
    expect(copyright_text).to_be_visible()