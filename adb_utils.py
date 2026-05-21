import subprocess
import re

def run_adb_command(command):
    """Executes an ADB command and returns the output."""
    result = subprocess.run(f"adb {command}", shell=True, capture_output=True, text=True)
    return result.stdout

def get_battery_temperature():
    """Gets battery temp. ADB returns it in tenths of a degree (e.g., 300 = 30.0 C)"""
    output = run_adb_command("shell dumpsys battery")
    match = re.search(r'temperature:\s*(\d+)', output)
    if match:
        return float(match.group(1)) / 10.0 
    return None

def get_network_signal_strength():
    """Gets Wi-Fi RSSI (Signal Strength)"""
    # ask for the whole wifi log without grep, making it safer across operating systems
    output = run_adb_command("shell dumpsys wifi")
    
    # (?i) makes it case-insensitive
    # [=:\s]* means it will match "rssi=-50", "RSSI: -50", "mRssi -50", etc
    match = re.search(r'(?i)rssi[=:\s]*(-?\d+)', output)
    
    if match:
        return int(match.group(1))
    return None


if __name__ == "__main__":
    print("Testing ADB Utils...")
    
    temp = get_battery_temperature()
    print(f"Battery Temp: {temp} °C")
    
    signal = get_network_signal_strength()
    print(f"WiFi Signal (RSSI): {signal} dBm")