import subprocess

def get_wifi_passwords():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True, universal_newlines = True).stdout
    profile_names = (line.split(":")[1][1:-1] for line in command_output.split("\n") if "All User Profile" in line)
    
    wifi_profiles = {}
    for profile_name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile_name], capture_output = True, universal_newlines = True).stdout
        if "Key Content" in profile_info:
            wifi_profile["ssid"] = profile_name
            wifi_profile["password"] = subprocess.run(["netsh", "wlan", "show", "profile", profile_name, "key=clear"], capture_output = True, universal_newlines = True).stdout.split("Key Content")[1].split("\n")[0].strip()
            wifi_profiles[profile_name] = wifi_profile
    
    return wifi_profiles

# Get WiFi passwords
wifi_passwords = get_wifi_passwords()
for profile, info in wifi_passwords.items():
    print(f"SSID: {info['ssid']}, Password: {info['password']}")
