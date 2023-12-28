import requests

class DomainIPInfo:
    
    def __init__(self, target):
        self.target = target

    def get_general_info(self):
        try:
            response = requests.get(f'https://geolocation-db.com/json/{self.target}&position=true')
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

    def get_whois_info(self):
        try:
            response = requests.get(f'https://api.whoislookupapi.com/v1/whois?identifier={self.target}')
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
