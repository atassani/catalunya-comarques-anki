from lxml import etree

# pip install lxml

def list_path_ids_in_comarques_group(svg_file_path):
    # Define the Inkscape namespace
    namespaces = {
        'svg': 'http://www.w3.org/2000/svg',
        'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
    }

    # Parse the SVG file
    tree = etree.parse(svg_file_path)
    root = tree.getroot()

    # Find the group with inkscape:label="Comarques"
    comarques_group = root.find(".//svg:g[@inkscape:label='Comarques']", namespaces=namespaces)

    if comarques_group is not None:
        # Iterate over path elements within the group and print their IDs
        for path in comarques_group.findall('.//svg:path', namespaces={'svg': 'http://www.w3.org/2000/svg'}):
            path_id = path.get('id')
            if path_id:
                print(f'Path ID: {path_id}')
    else:
        print("Group with inkscape:label='Comarques' not found.")

# Example usage
svg_file_path = 'svg/catalunya-toponims.svg'  # Replace with the path to your SVG file
list_path_ids_in_comarques_group(svg_file_path)