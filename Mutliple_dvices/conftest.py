import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from devices import DEVICES


@pytest.fixture(scope="function", params=DEVICES, ids=lambda d: d["udid"])
def device_info(request):
    return request.param


@pytest.fixture(scope="function")
def driver(device_info):
    print(f"\nRunning on device: {device_info['udid']} on port {device_info['port']}")

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = device_info["udid"]
    options.no_reset = True

    drv = webdriver.Remote(
        f"http://127.0.0.1:{device_info['port']}",
        options=options,
    )
    drv.implicitly_wait(10)

    yield drv

    drv.quit()