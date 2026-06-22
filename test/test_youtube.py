import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.youtube
def test_youtube_search(driver):

    wait = WebDriverWait(driver, 30)

    print("Launching YouTube...")

    # ✅ FIX: stable launch method (NO activate_app)
    driver.execute_script(
        "mobile: shell",
        {
            "command": "monkey",
            "args": [
                "-p",
                "com.google.android.youtube",
                "1"
            ]
        }
    )

    time.sleep(5)

    # Click Search
    wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search"))
    ).click()

    # Click Voice Search
    wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Voice search"))
    ).click()

    time.sleep(2)

    # Enter text via ADB
    import subprocess

    subprocess.run(
        ["adb", "-s", "fd5b6d88", "shell", "input", "text", "VJ%20Blogs"],
        check=True
    )

    subprocess.run(
        ["adb", "-s", "fd5b6d88", "shell", "input", "keyevent", "66"],
        check=True
    )

    time.sleep(5)

    # Click first video
    first_video = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.XPATH, "(//android.view.ViewGroup[@content-desc])[1]")
        )
    )

    first_video.click()

    time.sleep(5)

    assert True