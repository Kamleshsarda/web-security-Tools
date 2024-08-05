import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_user_input():
    url = input("Enter the URL to check for CSRF vulnerability: ")
    if not is_valid_url(url):
        print("Invalid URL. Please enter a valid URL.")
        return None
    return url

def get_forms(url, session):
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all("form"), response

def extract_csrf_token(form):
    inputs = form.find_all("input")
    for input in inputs:
        if input.attrs.get("name") and "csrf" in input.attrs.get("name").lower():
            return input.attrs.get("name"), input.attrs.get("value")
    return None, None

def submit_form_with_payload(action_url, session, payload):
    # Only use POST method for this test
    response = session.post(action_url, data=payload)
    return response

def is_csrf_vulnerable(response, payload):
    content = response.content.decode().lower()
    for key, value in payload.items():
        if value.lower() in content:
            return True
    return False

def main():
    url = get_user_input()
    if not url:
        return

    session = requests.Session()
    forms, initial_response = get_forms(url, session)
    
    if not forms:
        print("No forms found on the page.")
        return

    print(f"Found {len(forms)} forms on the page. Testing for CSRF vulnerability...")

    for form in forms:
        action = form.attrs.get("action")
        action_url = urljoin(url, action)

        # Extract CSRF token if present
        csrf_name, csrf_value = extract_csrf_token(form)
        if csrf_name:
            # Use a malicious token value for testing
            csrf_payload = {csrf_name: "malicious_token"}
        else:
            csrf_payload = {}

        # Construct payload with form fields
        inputs = form.find_all("input")
        for input in inputs:
            name = input.attrs.get("name")
            if name and name != csrf_name:
                value = input.attrs.get("value", "CSRFd")
                csrf_payload[name] = value

        # Submit the form with the CSRF payload
        response = submit_form_with_payload(action_url, session, csrf_payload)
        
        # Check if the CSRF payload was successful
        if is_csrf_vulnerable(response, csrf_payload):
            print(f"CSRF vulnerability detected in form action '{action}'! Payload was executed.")
        else:
            print(f"No CSRF vulnerability detected in form action '{action}' or payload was blocked.")

if __name__ == "__main__":
    main()
