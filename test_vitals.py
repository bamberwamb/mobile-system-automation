import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from adb_utils import get_battery_temperature, get_network_signal_strength

@pytest.fixture(scope="session")
def driver():
    """Setup Appium session"""
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    
    # Initialize driver (Appium server must be running locally on port 4723)
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    yield driver
    driver.quit()

def test_battery_thermal_levels(driver):
    """Validates battery is not overheating"""
    temp = get_battery_temperature()
    print(f"Current Battery Temp: {temp} °C")
    
    assert temp is not None, "Could not retrieve battery temperature"
    assert temp < 40.0, f"Device is overheating! Temp is {temp}°C"

def test_network_signal_strength(driver):
    """Validates device has a viable network connection"""
    rssi = get_network_signal_strength()
    print(f"Current WiFi RSSI: {rssi} dBm")
    
    assert rssi is not None, "Could not retrieve network signal"
    assert rssi > -85, f"Network signal is too weak: {rssi} dBm"