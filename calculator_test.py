from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

options = UiAutomator2Options().load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "ZA22372GVR",
    "appium:udid": "ZA22372GVR",
    "appium:noReset": True,
    "appium:appPackage": "com.google.android.calculator",
    "appium:appActivity": "com.android.calculator2.Calculator"
})

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

time.sleep(3)

# TC1 : 7 + 8 = 15
driver.find_element("id","com.google.android.calculator:id/digit_7").click()
driver.find_element("id","com.google.android.calculator:id/op_add").click()
driver.find_element("id","com.google.android.calculator:id/digit_8").click()
driver.find_element("id","com.google.android.calculator:id/eq").click()

result = driver.find_element("id","com.google.android.calculator:id/result_final").text
assert result == "15"
print("TC1 Passed :", result)

driver.find_element("id","com.google.android.calculator:id/clr").click()

# TC2 : 9 - 4 = 5
driver.find_element("id","com.google.android.calculator:id/digit_9").click()
driver.find_element("id","com.google.android.calculator:id/op_sub").click()
driver.find_element("id","com.google.android.calculator:id/digit_4").click()
driver.find_element("id","com.google.android.calculator:id/eq").click()

result = driver.find_element("id","com.google.android.calculator:id/result_final").text
assert result == "5"
print("TC2 Passed :", result)

driver.find_element("id","com.google.android.calculator:id/clr").click()

# TC3 : 7 × 8 = 56
driver.find_element("id","com.google.android.calculator:id/digit_7").click()
driver.find_element("id","com.google.android.calculator:id/op_mul").click()
driver.find_element("id","com.google.android.calculator:id/digit_8").click()
driver.find_element("id","com.google.android.calculator:id/eq").click()

result = driver.find_element("id","com.google.android.calculator:id/result_final").text
assert result == "56"
print("TC3 Passed :", result)

driver.find_element("id","com.google.android.calculator:id/clr").click()

driver.find_element("id","com.google.android.calculator:id/digit_8").click()
driver.find_element("id","com.google.android.calculator:id/op_div").click()
driver.find_element("id","com.google.android.calculator:id/digit_2").click()
driver.find_element("id","com.google.android.calculator:id/eq").click()

result = driver.find_element("id","com.google.android.calculator:id/result_final").text
assert result == "4"
print("TC4 Passed :", result)

driver.quit()

print("All Test Cases Passed")