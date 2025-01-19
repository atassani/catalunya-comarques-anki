import os
from lxml import etree
import cairosvg
from copy import deepcopy

def modify_svg_and_convert_to_png(input_svg_path):
    # Define namespaces
    namespaces = {
        'svg': 'http://www.w3.org/2000/svg',
        'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
    }

    # Parse the SVG file
    tree = etree.parse(input_svg_path)
    root = tree.getroot()

    # Find the group with inkscape:label="Comarques"
    comarques_group = root.find(".//svg:g[@inkscape:label='Comarques']", namespaces=namespaces)

    if comarques_group is not None:
        # Iterate over path elements within the group
        for path in comarques_group.findall('.//svg:path', namespaces=namespaces):
            path_id = path.get('id')
            if path_id:
                # Create a deep copy of the entire SVG tree
                modified_tree = deepcopy(tree)
                modified_root = modified_tree.getroot()

                # Find the corresponding path in the copied tree
                modified_comarques_group = modified_root.find(".//svg:g[@inkscape:label='Comarques']", namespaces=namespaces)
                modified_path = modified_comarques_group.find(f".//svg:path[@id='{path_id}']", namespaces=namespaces)

                if modified_path is not None:
                    # Modify the style attribute
                    style = modified_path.get('style', '')
                    # Update or add stroke and stroke-width properties
                    style_dict = dict(item.split(":") for item in style.split(";") if item)
                    style_dict.update({'stroke': 'red', 'stroke-width': '3'})
                    # Reconstruct the style attribute
                    new_style = ';'.join(f"{k}:{v}" for k, v in style_dict.items())
                    modified_path.set('style', new_style)

                    # Define output filenames
                    output_svg_path = f"catalunyaNew-{path_id}.svg"
                    output_png_path = f"catalunyaNew-{path_id}.png"

                    # Write the modified SVG to a new file
                    modified_tree.write(output_svg_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

                    # Convert the new SVG to PNG with specified width
                    cairosvg.svg2png(url=output_svg_path, write_to=output_png_path, output_width=800)

                    # Optionally, remove the temporary SVG file
                    os.remove(output_svg_path)

        print("SVG modification and PNG conversion completed successfully.")
    else:
        print("Group with inkscape:label='Comarques' not found.")

# Example usage
input_svg = 'catalunya-toponims.svg'  # Replace with the path to your SVG file
modify_svg_and_convert_to_png(input_svg)
