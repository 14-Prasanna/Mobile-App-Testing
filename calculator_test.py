from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time


def click_element(driver, wait, locators):
    """
    Try multiple locator strategies until one works.
    """
    for locator_type, locator_value in locators:
        try:
            element = wait.until(
                EC.element_to_be_clickable((locator_type, locator_value))
            )
            element.click()
            print(f"Clicked using: {locator_type} -> {locator_value}")
            return True

        except Exception:
            continue

    raise Exception(f"Unable to locate element using: {locators}")


options = UiAutomator2Options()

options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "Android"
options.udid = "fd5b6d88"
options.no_reset = True

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 20)

try:
    print("Opening home screen...")
    driver.press_keycode(3)

    time.sleep(2)

    print("Launching Calculator...")
    driver.activate_app("com.coloros.calculator")

    time.sleep(5)

    print("Current package:", driver.current_package)

    # Click 5
    click_element(driver, wait, [
        (AppiumBy.ID, "com.coloros.calculator:id/digit_5"),
        (AppiumBy.ACCESSIBILITY_ID, "5"),
        (AppiumBy.XPATH, '//*[@text="5"]'),
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("5")'
        )
    ])

    # Click +
    click_element(driver, wait, [
        (AppiumBy.ID, "com.coloros.calculator:id/op_add"),
        (AppiumBy.ACCESSIBILITY_ID, "+"),
        (AppiumBy.ACCESSIBILITY_ID, "plus"),
        (AppiumBy.XPATH, '//*[@text="+"]'),
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("+")'
        )
    ])

    # Click 7
    click_element(driver, wait, [
        (AppiumBy.ID, "com.coloros.calculator:id/digit_7"),
        (AppiumBy.ACCESSIBILITY_ID, "7"),
        (AppiumBy.XPATH, '//*[@text="7"]'),
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("7")'
        )
    ])

    # Click =
    click_element(driver, wait, [
        (AppiumBy.ID, "com.coloros.calculator:id/eq"),
        (AppiumBy.ACCESSIBILITY_ID, "="),
        (AppiumBy.ACCESSIBILITY_ID, "equals"),
        (AppiumBy.XPATH, '//*[@text="="]'),
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("=")'
        )
    ])

    time.sleep(2)

    result = None

    result_locators = [
        (AppiumBy.ID, "com.coloros.calculator:id/result"),
        (AppiumBy.ID, "com.coloros.calculator:id/formula"),
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().resourceIdMatches(".*result.*")'
        )
    ]

    for locator_type, locator_value in result_locators:
        try:
            result = wait.until(
                EC.presence_of_element_located(
                    (locator_type, locator_value)
                )
            )
            break
        except TimeoutException:
            continue

    if result:
        actual_result = result.text
        print("Result =", actual_result)

        if actual_result == "12":
            print("Test Passed")
        else:
            print("Test Failed")
    else:
        print("Result element not found")

except Exception as e:
    print("\nTest Failed")
    print(e)

    with open("calculator.xml", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    print("\nPage source saved as calculator.xml")

finally:
    time.sleep(5)
    driver.quit()