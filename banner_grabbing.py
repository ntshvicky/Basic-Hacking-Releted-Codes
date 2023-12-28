import socket

def grab_banner1(ip_address, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip_address, port))
            banner = s.recv(1024)
            return banner.decode().strip()
    except Exception as e:
        return f"Error: {e}"

def grab_banner2(ip_address, port):
    try:
        # Create a socket object
        socket.setdefaulttimeout(2)
        s = socket.socket()
        
        # Connect to the server
        s.connect((ip_address, port))
        
        # Send a basic HTTP request, if needed. Adjust for other protocols.
        s.send(b'GET HTTP/1.1 \r\n')
        
        # Receive the banner
        banner = s.recv(1024)
        
        return banner
    except Exception as e:
        return f"Error: {e}"
    
# Example usage
ip = '18.156.60.243' # Replace with the target IP or hostname
port = 8001        # Replace with the target port
print(grab_banner2(ip, port))
