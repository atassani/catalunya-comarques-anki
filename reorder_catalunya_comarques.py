import re

def reorder_and_correct_numbering(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Preserve the heading and footer
    heading_pattern = re.compile(r'^(# Comarques de Catalunya\n\n---\n\nDeck: Comarques de Catalunya\nTags: catalunya\n\n)', re.DOTALL)
    footer_pattern = re.compile(r'(\n---\n)$', re.DOTALL)

    heading_match = heading_pattern.search(content)
    footer_match = footer_pattern.search(content)

    if not heading_match or not footer_match:
        raise ValueError("The file does not contain the expected heading or footer format.")

    heading = heading_match.group(1)
    footer = footer_match.group(1)
    body = content[len(heading):-len(footer)].strip()

    # Regex to match and capture each Q&A pair, ensuring we handle cases like "Lluçanès"
    pattern = re.compile(
        r'(<!--ID:\d*-->\n\d+\. Quina és la capital de la comarca (del |de l\'|de la |de les |d\'|de )\*\*(.*?)\*\*\?\n'
        r'> La capital de la comarca (del |de l\'|de la |de les |d\'|de ).*? és \*\*(.*?)\*\*.\n>\n'
        r'> !\[.*?\]\(.*?\)\n\n'
        r'<!--ID:\d*-->\n\d+\. De quina comarca \*\*(.*?)\*\* és la capital\?\n'
        r'> .*? és la capital (del |de l\'|de la |de les |d\'|de )\*\*(.*?)\*\*.\n>\n'
        r'> !\[.*?\]\(.*?\)\n?)',  # Handle optional newline at the end
        re.DOTALL
    )

    # Extract all Q&A pairs
    matches = pattern.findall(body)

    # Debugging: Check if "Alt Camp" and "Lluçanès" are captured
    debug_comarques = [match[2] for match in matches]
    if "Alt Camp" not in debug_comarques:
        print("Debug: 'Alt Camp' was not captured. Please review the pattern.")
    if "Lluçanès" not in debug_comarques:
        print("Debug: 'Lluçanès' was not captured. Please review the pattern.")

    # Create a list of tuples (comarca_name, full_match_content)
    qna_pairs = [
        (match[2], match[0]) for match in matches
    ]

    # Sort by comarca names alphabetically
    qna_pairs.sort(key=lambda x: x[0])

    # Reconstruct the content with corrected numbering
    new_content = heading
    counter = 1
    for comarca_name, full_match in qna_pairs:
        # Update numbering sequentially while preserving the ID
        updated_content = re.sub(r'(\d+)\.', f'{counter}.', full_match, count=1)
        updated_content = re.sub(r'(\n<.*>\n)(\d+)\.', lambda m: f'{m.group(1)}{counter + 1}.' , updated_content, count=1)
        new_content += updated_content + "\n\n"
        counter += 2  # Increment by 2 for each Q&A pair
    new_content += footer

    # Overwrite the original file with reordered and renumbered content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print(f"\nFile has been reordered and renumbered successfully.")

# Path to the markdown file
markdown_file_path = 'output/catalunya.md'

# Execute the script to reorder and renumber the Markdown content
reorder_and_correct_numbering(markdown_file_path)
