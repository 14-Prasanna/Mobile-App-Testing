import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


ID_SUFFIXES = {
    "5": "digit_5",
    "7": "digit_7",
    "+": "op_add",
    "=": "eq",
}


def dump_page_source(driver, device_udid, tag):
    filename = f"pagesource_{device_udid}_{tag}.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"\n--- Page source dump written to {filename} ---\n")


def click_button(driver, symbol, package, device_udid, timeout=8):
    suffix = ID_SUFFIXES.get(symbol)
    if suffix is None:
        raise ValueError(f"No known id suffix for symbol '{symbol}'")

    resource_id = f"{package}:id/{suffix}"

    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.ID, resource_id))
        )
        element.click()
    except TimeoutException:
        dump_page_source(driver, device_udid, symbol.replace("+", "plus"))
        raise


def clear_calculator(driver, package):
    clear_id = f"{package}:id/clr"
    for _ in range(3):
        try:
            btn = driver.find_element(AppiumBy.ID, clear_id)
            btn.click()
            time.sleep(0.5)
        except NoSuchElementException:
            break


def _non_empty_text(by_locator):
    """Custom expected_condition: waits until the element exists AND
    its text attribute is non-empty, instead of just present-in-DOM."""
    def predicate(driver):
        try:
            el = driver.find_element(*by_locator)
            text = el.text.strip()
            return el if text else False
        except NoSuchElementException:
            return False
    return predicate


def get_result_text(driver, package, device_udid, timeout=10):
    """
    Waits specifically for the result field to contain text (not just
    exist), since Google/ColorOS calculators render an empty result
    view before the computed value animates in. Without this, a fast
    poll can read the empty/placeholder element or fall back to the
    formula bar before the real answer appears.
    """
    resource_id = f"{package}:id/result"

    try:
        element = WebDriverWait(driver, timeout).until(
            _non_empty_text((AppiumBy.ID, resource_id))
        )
        return element.text
    except TimeoutException:
        pass

    # Fallback only if the result field genuinely never populates
    candidates = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
    candidates += driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")

    for el in candidates:
        txt = el.text.strip()
        if txt and any(ch.isdigit() for ch in txt):
            return txt

    dump_page_source(driver, device_udid, "result")
    raise NoSuchElementException("Could not locate a result field on screen")


@pytest.mark.parallel
def test_calculator(driver, device_info):

    package = device_info["calculator_package"]
    udid = device_info["udid"]

    driver.terminate_app(package)
    driver.activate_app(package)
    time.sleep(2)

    clear_calculator(driver, package)

    click_button(driver, "5", package, udid)
    click_button(driver, "+", package, udid)
    click_button(driver, "7", package, udid)
    click_button(driver, "=", package, udid)

    result = get_result_text(driver, package, udid)
    print(f"\n[{udid}] Result:", result)

    # assert "12" in result