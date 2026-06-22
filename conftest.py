import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
def driver():

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android"
    options.udid = "fd5b6d88"

    options.no_reset = True
    options.full_reset = False

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    driver.implicitly_wait(10)

    yield driver

    driver.quit()