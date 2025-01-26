from lxml import etree as ET

def create_combined_svg(base_svg_path, new_svg_path, output_svg_path):
    # Parse the base and new SVG files
    base_svg = ET.parse(base_svg_path)
    new_svg = ET.parse(new_svg_path)

    # Get the root elements
    base_root = base_svg.getroot()
    new_root = new_svg.getroot()

    # Remove viewBox from the base SVG and set the width and height explicitly
    base_root.attrib.pop("viewBox", None)
    base_root.set("width", "800")
    base_root.set("height", "775")

    # Extract the <defs> and <g id="FullCatNord"> from the new SVG
    new_defs = new_root.find(".//{http://www.w3.org/2000/svg}defs")
    full_cat_nord = new_root.find(".//{http://www.w3.org/2000/svg}g[@id='FullCatNord']")

    # Insert the style element from <defs> of the new SVG into the base SVG's <defs>
    base_defs = base_root.find(".//{http://www.w3.org/2000/svg}defs")
    if base_defs is None:
        base_defs = ET.SubElement(base_root, "defs", nsmap={"": "http://www.w3.org/2000/svg"})

    if new_defs is not None:
        new_styles = new_defs.find(".//{http://www.w3.org/2000/svg}style")
        if new_styles is not None:
            base_defs.append(new_styles)

    # Transform the <g id="FullCatNord"> to align with the base SVG's dimensions
    if full_cat_nord is not None:
        new_viewbox = new_root.attrib.get("viewBox", "0 0 791.0743 765.1844")
        new_width = float(new_root.attrib.get("width", "791.0743"))
        new_height = float(new_root.attrib.get("height", "765.1844"))

        # Base SVG dimensions
        base_width = 800
        base_height = 775

        # Extract the viewBox values
        vb_min_x, vb_min_y, vb_width, vb_height = map(float, new_viewbox.split())

        # Calculate scaling factors and translation
        scale_x = base_width / vb_width
        scale_y = base_height / vb_height
        scale = min(scale_x, scale_y)  # Uniform scaling
        translate_x = -vb_min_x * scale
        translate_y = -vb_min_y * scale

        # Apply transformation to the group
        transform = f"translate({translate_x} {translate_y}) scale({scale})"
        full_cat_nord.set("transform", transform)

        # Insert the transformed <g> before the first <g> element in the base SVG
        first_g = base_root.find(".//{http://www.w3.org/2000/svg}g")
        if first_g is not None:
            parent = first_g.getparent()
            parent.insert(parent.index(first_g), full_cat_nord)

    # Save the combined SVG
    base_svg.write(output_svg_path, encoding="utf-8", xml_declaration=True)

# Paths to the SVG files
base_svg_path = "svg/catalunya.svg"
new_svg_path = "svg/LluçanèsACatalunya23.svg"
output_svg_path = "svg/combined_catalunya.svg"

# Create the combined SVG
create_combined_svg(base_svg_path, new_svg_path, output_svg_path)
