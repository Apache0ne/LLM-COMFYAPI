import html

def escape_html(content):
    """Escape HTML special characters in the given content."""
    return html.escape(content)

def sanitize_html(content):
    """Sanitize HTML content to prevent XSS attacks."""
    # This is a basic example of sanitization. For more robust sanitization, consider using a library like bleach.
    return html.escape(content)