from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Function to crawl the website and find URLs
def crawl_website(base_url):
    urls_to_test = set()
    urls_to_visit = set([base_url])

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a'):
                href = link.get('href')
                if href and not href.startswith('http'):
                    href = urljoin(base_url, href)
                if href.startswith(base_url):
                    urls_to_visit.add(href)
                    urls_to_test.add(href)

        except requests.RequestException:
            # Handle exceptions for requests
            pass

    return list(urls_to_test)


# List of simple payloads for testing SQL Injection and XSS
sql_injection_payloads = ["'", '"', "'; --", '"; --']
xss_payloads = ['<script>alert(1)</script>', '"<script>alert(1)</script>', "'<script>alert(1)</script>"]

# Function to check if a payload potentially causes a vulnerability
def is_vulnerable(response):
    # You can add logic to check for specific indications of vulnerabilities
    # For example, error messages in the response, status codes, etc.
    error_messages = ["MySQL syntax", "SQL syntax", "Query failed"]
    for error in error_messages:
        if error in response.text:
            return True
    return False

# Function to test a single URL for vulnerabilities
def test_url(url):
    vulnerabilities = []
    # Test for SQL Injection
    for payload in sql_injection_payloads:
        try:
            response = requests.get(url, params={'input': payload})
            if is_vulnerable(response):
                vulnerabilities.append(f"Potential SQL Injection found at {url} with payload {payload}")
        except requests.RequestException:
            pass

    # Test for XSS
    for payload in xss_payloads:
        try:
            response = requests.get(url, params={'input': payload})
            if payload in response.text:
                vulnerabilities.append(f"Potential XSS found at {url} with payload {payload}")
        except requests.RequestException:
            pass

    return vulnerabilities

# Main function
def main():
    target_url = "full-website-url"  # Replace with the target URL
    urls_to_crawl = crawl_website(target_url)

    print(urls_to_crawl)
    all_vulnerabilities = []
    for url in urls_to_crawl:
        vulnerabilities = test_url(url)
        all_vulnerabilities.extend(vulnerabilities)

    # Generate a report
    for vulnerability in all_vulnerabilities:
        print(vulnerability)

if __name__ == "__main__":
    main()
