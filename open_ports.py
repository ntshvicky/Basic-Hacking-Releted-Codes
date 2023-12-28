import socket
import concurrent.futures
from tqdm import tqdm

def get_service_name(port, protocol='tcp'):
    try:
        service_name = socket.getservbyport(port, protocol)
    except OSError:
        service_name = 'Unknown'
    return service_name

def check_port(ip, port, payload):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip, port))

            banner = '-'
            try:
                banner = s.recv(1024).decode().strip()
                print(banner)
            except socket.timeout:
                pass
            
            service_name = 'Unknown'
            
            try:
                service_name = socket.getservbyport(port, 'tcp')
            except OSError:
                pass
            

            s.sendall(payload.encode())
            response = s.recv(1024)
            return {port: {
                        "service_name": service_name, 
                        "payload_response": response, 
                        "banner_footprint": banner
                    }}, True
    except Exception as e:
        print(f"Exception in port {port}: {e}")
        return {port: None}, False

def scan_ports_concurrent(ip, port_range, payload):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(check_port, ip, port, payload): port for port in range(*port_range)}
        for future in tqdm(concurrent.futures.as_completed(future_to_port), total=len(future_to_port), unit="port"):
            port_resp, is_open = future.result()
            if is_open:
                open_ports.append(port_resp)

    return open_ports

# Example Usage
ip_address = '192.168.0.100'  # Replace with the target IP
port_range = (1, 65566)  # Standard range can be adjusted

port_range = (79, 9000) 

open_ports = scan_ports_concurrent(ip_address, port_range, "Hello World!")
print("Open ports:", open_ports)
