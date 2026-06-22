from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess
import time

options = UiAutomator2Options()

options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "Android"
options.udid = "fd5b6d88"

options.app_package = "com.google.android.youtube"
options.app_activity = "com.google.android.youtube.app.honeycomb.Shell$HomeActivity"

options.no_reset = True

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 30)

try:
    print("Current package:", driver.current_package)

    # Click search icon
    print("Clicking search icon...")

    wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ACCESSIBILITY_ID, "Search")
        )
    ).click()

    # Click voice search
    print("Clicking voice search...")

    wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ACCESSIBILITY_ID, "Voice search")
        )
    ).click()

    time.sleep(2)

    # Input text using ADB
    print("Entering search text...")

    subprocess.run(
        [
            "adb",
            "-s",
            "fd5b6d88",
            "shell",
            "input",
            "text",
            "VJ%20Blogs"
        ],
        check=True
    )

    # Press Enter
    subprocess.run(
        [
            "adb",
            "-s",
            "fd5b6d88",
            "shell",
            "input",
            "keyevent",
            "66"
        ],
        check=True
    )

    print("Search executed")

    time.sleep(5)

    # Click first video
    print("Opening first video...")

    first_video = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                "(//android.view.ViewGroup[@content-desc])[1]"
            )
        )
    )

    first_video.click()

    print("First video opened")

    time.sleep(10)

except Exception as e:
    print("Test Failed")
    print(e)

    with open("youtube_page_source.xml", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("Page source saved as youtube_page_source.xml")

finally:
    driver.quit()