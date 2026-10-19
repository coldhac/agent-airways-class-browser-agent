from playwright.sync_api import Page

def select_seat(page: Page, seat_id: str) -> dict:
    if not seat_id or not isinstance(seat_id, str):
        raise ValueError("Invalid seat identifier provided.")

    formatted_seat = seat_id.strip().upper()
    locator = page.locator(f"button:has-text('{formatted_seat}'), [data-seat='{formatted_seat}']").first

    if locator.count() == 0 or not locator.is_visible():
        raise RuntimeError(f"Seat {formatted_seat} does not exist or seat map is not loaded.")

    if locator.get_attribute("disabled") is not None or locator.get_attribute("aria-disabled") == "true":
        raise RuntimeError(f"Seat {formatted_seat} is occupied or unavailable.")

    locator.click()

    class_attr = locator.get_attribute("class") or ""
    aria_checked = locator.get_attribute("aria-checked") or ""
    is_selected = "selected" in class_attr or aria_checked == "true"

    if not is_selected:
        raise AssertionError(f"Verification failed: Seat {formatted_seat} was not selected.")

    return {"status": "success", "selected_seat": formatted_seat}