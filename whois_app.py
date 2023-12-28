import whois_app

def get_domain_whois(domain):
    try:
        w = whois_app.whois_app(domain)
        return w
    except Exception as e:
        return str(e)

# Example Usage
domain = 'nitishsrivastava.in'
print(get_domain_whois(domain))

