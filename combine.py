import re
import html

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

def merge_html_files(file1_path, file2_path, output_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        html1 = file1.read()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        html2 = file2.read()

    # Update margin in the body div for each file
    html1 = update_margin_in_body(html1)
    html2 = update_margin_in_body(html2)

    # Escape HTML content to be safely used within srcdoc attribute
    escaped_html1 = escape_html_for_srcdoc(html1)
    escaped_html2 = escape_html_for_srcdoc(html2)

    # Create the merged HTML
    merged_html = f"""
    <!DOCTYPE html>
    <html lang='fr'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Combined H5P Content</title>
        <style>
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
                border: none;
                display: block;
                overflow: hidden;
                scrollbar-width: none;
            }}
            iframe::-webkit-scrollbar {{
                display: none;
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
        <h1>Combined H5P Content</h1>

        <!-- First HTML File Content -->
        <div class='content-block' style="margin: 0;">
            <iframe srcdoc="{escaped_html1}" onload="resizeIframe(this)"></iframe>
        </div>

        <!-- Second HTML File Content -->
        <div class='content-block' style="margin: 0;">
            <iframe srcdoc="{escaped_html2}" onload="resizeIframe(this)"></iframe>
        </div>
    </body>
    </html>
    """

    # Write the merged HTML to the output file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(merged_html)

# Example usage
merge_html_files('1-Tour de magie.html', "2-J'ai déjà appris.html", 'combined.html')
