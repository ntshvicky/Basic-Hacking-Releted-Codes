import socket

# Define the range of IP addresses to scan
ip_range = "192.168.0."
start_ip = 100
end_ip = 300

# Function to check if a host is online
def is_host_online(ip, port):
    try:
        print(f"Checking if host {ip}:{port} is online")
        socket.setdefaulttimeout(1)  # Adjust the timeout as needed
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

# Scan the IP range
for i in range(start_ip, end_ip + 1):
    ip = ip_range + str(i)
    if is_host_online(ip, 80):  # Check port 80 (HTTP) for example
        print(f"Host {ip} is online.")
