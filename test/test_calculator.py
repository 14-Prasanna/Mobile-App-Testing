import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_element(driver, wait, locators):
    for locator_type, locator_value in locators:
        try:
            element = wait.until(
                EC.element_to_be_clickable((locator_type, locator_value))
            )
            element.click()
            return
        except Exception:
            continue
    raise Exception("Element not found")


@pytest.mark.calculator
def test_calculator_addition(driver):

    wait = WebDriverWait(driver, 20)

    driver.press_keycode(3)  # Home
    time.sleep(2)

    driver.activate_app("com.coloros.calculator")
    time.sleep(3)

    click_element(driver, wait, [
        (AppiumBy.ID, "com.coloros.calculator:id/digit_5"),
        (AppiumBy.XPATH, '//*[@text="5"]')
    ])

    click_element(driver, wait, [
        (AppiumBy.ID, "com.coloros.calculator:id/op_add"),
        (AppiumBy.XPATH, '//*[@text="+"]')
    ])

    click_element(driver, wait, [
        (AppiumBy.ID, "com.coloros.calculator:id/digit_7"),
        (AppiumBy.XPATH, '//*[@text="7"]')
    ])

    click_element(driver, wait, [
        (AppiumBy.ID, "com.coloros.calculator:id/eq"),
        (AppiumBy.XPATH, '//*[@text="="]')
    ])

    time.sleep(2)

    result = driver.find_element(
        AppiumBy.ID,
        "com.coloros.calculator:id/result"
    ).text

    print("Result:", result)

    assert "12" in result

    driver.press_keycode(4)