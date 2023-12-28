import subprocess

def get_wifi_passwords():
    try:
        command_output = subprocess.run(["networksetup", "-listnetworkserviceorder"], capture_output=True, text=True).stdout
        wifi_service_line = [line for line in command_output.split("\n") if "Wi-Fi" in line and "Device:" in line][0]
        print(wifi_service_line)
        device_name = wifi_service_line.split(", Device: ")[1].replace(")", "").strip()
        
        ssid_output = subprocess.run(["networksetup", "-getairportnetwork", device_name], capture_output=True, text=True).stdout
        ssid = ssid_output.split(": ")[1].strip()
        
        password_output = subprocess.run(["security", "find-generic-password", "-D", "AirPort network password", "-wa", ssid], capture_output=True, text=True).stdout
        password = password_output.strip()
        
        wifi_profiles = {ssid: password}
        
        return wifi_profiles
    except Exception as e:
        return str(e)

# Get WiFi passwords
wifi_passwords = get_wifi_passwords()
print(wifi_passwords)
