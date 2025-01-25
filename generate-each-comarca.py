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
    comarques_group = root.find(".//svg:g[@id='Comarques']", namespaces=namespaces)

    if comarques_group is not None:
        # Iterate over path elements within the group
        for element in comarques_group.xpath(".//svg:path | .//svg:polygon", namespaces=namespaces):
            element_id = element.get('id')
            if element_id:

                # Create a deep copy of the entire SVG tree
                modified_tree = deepcopy(tree)
                modified_root = modified_tree.getroot()

                # Find the corresponding path in the copied tree
                modified_comarques_group = modified_root.find(".//svg:g[@id='Comarques']", namespaces=namespaces)
                modified_path = modified_comarques_group.xpath(f".//svg:path[@id='{element_id}'] | .//svg:polygon[@id='{element_id}']", namespaces=namespaces)
                islands_path =  modified_comarques_group.xpath(f".//svg:path[starts-with(@id, 'island') and contains(@id, '{element_id}')]", namespaces=namespaces)
                paths_to_change = modified_path + islands_path

                if element_id.startswith('island'):
                    continue

                if len(paths_to_change) > 0:
                    for element in paths_to_change:
                        # Modify the style attribute
                        element.set("style", "stroke: red; stroke-width: 3;")

                    # Convert hyphens to underscores in element_id
                    element_id = element_id.replace('-', '_')
                    print(f"Converted element_id: {element_id}")

                    # Define output filenames
                    output_svg_path = f"output/images/catalunya_{element_id}.svg"
                    output_png_path = f"output/images/catalunya_{element_id}.png"

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
input_svg = 'svg/catalunya-toponims.svg'  # Replace with the path to your SVG file
modify_svg_and_convert_to_png(input_svg)
