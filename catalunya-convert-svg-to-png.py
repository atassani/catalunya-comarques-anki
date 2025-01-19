import cairosvg

def svg_to_png(input_svg_path, output_png_path, output_width=800):
    # Convert SVG to PNG with specified width
    cairosvg.svg2png(
        url=input_svg_path,
        write_to=output_png_path,
        output_width=output_width
    )

# Example usage
input_svg = 'catalunya-toponims.svg'  # Path to your input SVG file
output_png = 'catalunya-toponims.png'  # Path to save the output PNG file

svg_to_png(input_svg, output_png)