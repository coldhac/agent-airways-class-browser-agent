from playwright.sync_api import sync_playwright
from team_tools.select_seat import select_seat

def setup_page_to_seat_selection(page):
    page.goto("https://onyourmark.github.io/browser-agent-form/travel/")
    page.wait_for_load_state("networkidle")
    
    search_btn = page.locator("button:has-text('Search'), input[type='submit']").first
    if search_btn.count() > 0 and search_btn.is_visible():
        search_btn.click()
        page.wait_for_timeout(1000)

    choose_flight_btn = page.locator("button:has-text('Select'), button:has-text('Choose')").first
    if choose_flight_btn.count() > 0 and choose_flight_btn.is_visible():
        choose_flight_btn.click()
        page.wait_for_timeout(1000)

def test_select_seat_normal():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        setup_page_to_seat_selection(page)
        
        available_seat = page.locator("div[aria-label='Airplane seat map'] button:not([disabled])").first
        if available_seat.count() > 0:
            seat_name = available_seat.inner_text().strip()
            result = select_seat(page, seat_name)
            assert result["status"] == "success"
        browser.close()

def test_select_seat_failure():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        setup_page_to_seat_selection(page)

        try:
            select_seat(page, "NON_EXISTENT_999")
            assert False, "Expected error for invalid seat"
        except RuntimeError as e:
            assert "does not exist" in str(e)

        browser.close()