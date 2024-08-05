import requests
from bs4 import BeautifulSoup

def check_csrf_vulnerability(url):
    session = requests.Session()
    
    # Step 1: Retrieve the page content
    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    # Step 2: Parse the page content to find forms
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')
    if not forms:
        print("No forms found on the page.")
        return
    
    for form in forms:
        action = form.get('action')
        if not action:
            continue
        
        form_url = url + action if action.startswith('/') else action
        method = form.get('method', 'get').lower()
        
        # Step 3: Extract form inputs and CSRF tokens
        inputs = form.find_all('input')
        form_data = {}
        csrf_token_name = None
        for input_tag in inputs:
            name = input_tag.get('name')
            value = input_tag.get('value', '')
            form_data[name] = value
            if 'csrf' in name.lower():
                csrf_token_name = name
        
        if csrf_token_name:
            print(f"Found CSRF token: {csrf_token_name}")
            # Step 4: Remove CSRF token and submit the form
            del form_data[csrf_token_name]
            if method == 'post':
                response = session.post(form_url, data=form_data)
            else:
                response = session.get(form_url, params=form_data)
            
            if response.status_code == 200:
                print(f"Form submission without CSRF token succeeded. The site is likely vulnerable to CSRF.")
            else:
                print(f"Form submission without CSRF token failed. The site might be protected against CSRF.")
        else:
            print("No CSRF token found in the form.")
        
        # Print a separator for readability
        print("-" * 40)

# Example usage
url = input("Enter the URL to check for CSRF vulnerability: ")
check_csrf_vulnerability(url)