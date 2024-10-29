import re
import html
import os

def escape_single_quotes(text):
    return text.replace("'", "\\'")

def escape_double_quotes(text):
    return text.replace('"', '\\"')

def escape_html_for_srcdoc(text):
    # Escape only quotes to avoid breaking the srcdoc attribute, but keep HTML tags intact
    return text.replace("'", "&#39;").replace('"', "&quot;")

def update_margin_in_body(html_content):
    # Replace the margin style in the main div inside the body
    return re.sub(r'(<div style=")margin: 20px 20px;', r'\1margin: 0;', html_content, flags=re.DOTALL)

def merge_html_files_in_directory(directory_path):
    print(f"Looking for HTML files in directory: {directory_path}")

    # Extract directory name for title and header
    directory_name = os.path.basename(directory_path).replace('-', ' ')

    # Get all HTML files starting with a number in consecutive order
    html_files = sorted(
        [f for f in os.listdir(directory_path) if re.match(r'^\d+.*\.html$', f)],
        key=lambda x: int(re.match(r'^(\d+)', x).group(1))
    )

    if not html_files:
        print("No HTML files found that start with a number.")
        return

    print(f"Found HTML files: {html_files}")

    merged_html_content = f"""
<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>{directory_name}</title>
    <style>
        body {{
            font-family:Sans-Serif;
        }}
        /* Add some basic styles to separate content visually */
        .content-block {{
            margin: 0;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
            display: block;
            overflow: hidden;
        }}
        iframe {{
            width: 100%;
            border: 0;
            display: block;
            overflow: hidden;
            scrollbar-width: none;
        }}
        iframe::-webkit-scrollbar {{
            display: none;
        }}
        .divider {{
            width: 100%;
            border-top: 2px dashed #000;
            margin: 20px 0;
        }}
        h2 {{
            adding: 20px 0 0 0;
            text-align: center;
            color: #1a73d9;
            border-top: 4px solid #1a73d9;
            margin-top: 40px;
            padding-top:20px;
        }}
    </style>
    <script>
        function resizeIframe(iframe) {{
            iframe.style.height = (iframe.contentWindow.document.body.scrollHeight + 50) + 'px';
            setTimeout(function() {{
                iframe.style.height = (iframe.contentWindow.document.body.scrollHeight + 50) + 'px';
            }}, 500);
        }}
    </script>
</head>
<body>
    <h1 style="text-align:center;">{directory_name}</h1>
"""

    # Read each HTML file and add to the merged content
    for html_file in html_files:
        print(f"Processing file: {html_file}")
        with open(os.path.join(directory_path, html_file), 'r', encoding='utf-8') as file:
            html_content = file.read()
            updated_html_content = update_margin_in_body(html_content)
            escaped_html_content = escape_html_for_srcdoc(updated_html_content)
            file_number = re.match(r'^(\d+)', html_file).group(1)
            file_name_without_number = re.sub(r'^\d+-', '', html_file).rsplit('.', 1)[0]
            merged_html_content += f"""
    <h2>{file_number}. {file_name_without_number}</h2>
    <div class='content-block' style="margin: 0;">
        <iframe srcdoc="{escaped_html_content}" onload="resizeIframe(this)" style="width: 100%; border: 0;"></iframe>
    </div>
    """

    # Close the HTML structure
    merged_html_content += """
</body>
</html>
"""

    # Write the merged HTML to the output file
    output_path = os.path.join(directory_path, 'index.html')
    print(f"Writing merged content to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(merged_html_content)
    print("Merging complete.")

# Example usage
# merge_html_files_in_directory('/path/to/your/directory')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python merge_html_files.py <directory_path>")
    else:
        merge_html_files_in_directory(sys.argv[1])
