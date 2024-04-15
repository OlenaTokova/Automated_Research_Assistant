import re

def sanitize_filename(filename):
    """
    Sanitize the query to be used as a valid filename.
    """
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')
