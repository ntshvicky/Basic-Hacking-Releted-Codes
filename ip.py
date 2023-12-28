import requests

class IPLocation:
    
    def get_ip_address(self):
        response = requests.get('https://api.ipify.org?format=json')
        ip_address = response.json()['ip']
        return ip_address

    def get_ip_location(self, ip_address):
        response = requests.get(f'https://geolocation-db.com/json/{ip_address}&position=true')
        location_data = response.json()
        return location_data

    def get_location(self):
        ip_address = self.get_ip_address()
        location_data = self.get_ip_location(ip_address)
        return location_data



