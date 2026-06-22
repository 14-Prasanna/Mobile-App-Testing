from appium import webdriver
from appium.options.android import UiAutomator2Options
from threading import Thread
import time


def run_calculator_test(udid, port):

    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": udid,
        "appium:udid": udid,
        "appium:noReset": True,
        "appium:appPackage": "com.google.android.calculator",
        "appium:appActivity": "com.android.calculator2.Calculator"
    })

    driver = webdriver.Remote(
        f"http://127.0.0.1:{port}",
        options=options
    )

    time.sleep(2)

    print(f"\nRunning on Device: {udid}")

    # ----------------------------
    # Test Case 1 : 7 × 8 = 56
    # ----------------------------
    driver.find_element("id", "com.google.android.calculator:id/digit_7").click()
    driver.find_element("id", "com.google.android.calculator:id/op_mul").click()
    driver.find_element("id", "com.google.android.calculator:id/digit_8").click()
    driver.find_element("id", "com.google.android.calculator:id/eq").click()

    result = driver.find_element(
        "id",
        "com.google.android.calculator:id/result_final"
    ).text

    assert result == "56"
    print(f"{udid} - TC1 Passed - Result: {result}")

    driver.find_element("id", "com.google.android.calculator:id/clr").click()

    # ----------------------------
    # Test Case 2 : 6 + 2 = 8
    # ----------------------------
    driver.find_element("id", "com.google.android.calculator:id/digit_6").click()
    driver.find_element("id", "com.google.android.calculator:id/op_add").click()
    driver.find_element("id", "com.google.android.calculator:id/digit_2").click()
    driver.find_element("id", "com.google.android.calculator:id/eq").click()

    result = driver.find_element(
        "id",
        "com.google.android.calculator:id/result_final"
    ).text

    assert result == "8"
    print(f"{udid} - TC2 Passed - Result: {result}")

    driver.find_element("id", "com.google.android.calculator:id/clr").click()

    # ----------------------------
    # Test Case 3 : 10 - 20 = -10
    # ----------------------------
    driver.find_element("id", "com.google.android.calculator:id/digit_1").click()
    driver.find_element("id", "com.google.android.calculator:id/digit_0").click()

    driver.find_element("id", "com.google.android.calculator:id/op_sub").click()

    driver.find_element("id", "com.google.android.calculator:id/digit_2").click()
    driver.find_element("id", "com.google.android.calculator:id/digit_0").click()

    driver.find_element("id", "com.google.android.calculator:id/eq").click()

    result = driver.find_element(
        "id",
        "com.google.android.calculator:id/result_final"
    ).text

    assert result == "-10"
    print(f"{udid} - TC3 Passed - Result: {result}")

    driver.find_element("id", "com.google.android.calculator:id/clr").click()

    # ----------------------------
    # Test Case 4 : 8 ÷ 2 = 4
    # ----------------------------
    driver.find_element("id", "com.google.android.calculator:id/digit_8").click()

    driver.find_element("id", "com.google.android.calculator:id/op_div").click()

    driver.find_element("id", "com.google.android.calculator:id/digit_2").click()

    driver.find_element("id", "com.google.android.calculator:id/eq").click()

    result = driver.find_element(
        "id",
        "com.google.android.calculator:id/result_final"
    ).text

    assert result == "4"
    print(f"{udid} - TC4 Passed - Result: {result}")

    driver.quit()


# Device 1
t1 = Thread(
    target=run_calculator_test,
    args=("00196659G000968", 4723)
)

# Device 2
t2 = Thread(
    target=run_calculator_test,
    args=("ZD222QX5X4", 4725)
)

t1.start()
t2.start()

t1.join()
t2.join()

print("\nExecution Completed on Both Devices")