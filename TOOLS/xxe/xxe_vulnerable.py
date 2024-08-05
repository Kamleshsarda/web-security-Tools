import xml.etree.ElementTree as ET

def parse_xml(xml_content):
    try:
        # Parse the XML content
        root = ET.fromstring(xml_content)
        print("Parsed XML content:")
        print(ET.tostring(root, encoding='unicode'))
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")

if __name__ == "__main__":
    # Read XML content from file
    with open('payload.xml', 'r') as file:
        xml_data = file.read()

    # Print the original XML content
    print("Original XML content:")
    print(xml_data)

    # Parse the XML content
    parse_xml(xml_data)
