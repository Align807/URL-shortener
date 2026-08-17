# filepath: c:\Users\align\Downloads\02-ambiguous-url-shortener\02-ambiguous-url-shortener\app\server.py
from flask import Flask, request, jsonify, redirect, abort, send_from_directory
import random
import string
import os
import re
from urllib.parse import urlparse

# Server-side URL regex (allows http/https, domains, localhost, IPv4, optional port/path/query)
URL_REGEX = re.compile(
    r'^(https?://)'
    r'((([A-Za-z0-9\-]+)\.)+[A-Za-z]{2,}|localhost|(\d{1,3}\.){3}\d{1,3})'
    r'(:\d+)?(\/[^\s]*)?$',
    re.IGNORECASE,
)

app = Flask(__name__)

# In-memory store for URL mappings
_store = {}

def generate_code(length=6):
    """Generate a random short code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def is_valid_url(url: str) -> bool:
    """Basic URL validation: must have http/https scheme and a netloc."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.netloc:
            return False
        if len(url) > 2000:
            return False
        # Regex check for a stricter validation (domain, localhost, or IPv4)
        if not URL_REGEX.match(url):
            return False
        return True
    except Exception:
        return False


def is_valid_code(code: str, min_len: int = 4, max_len: int = 16) -> bool:
    """Validate short code format: alphanumeric and within length bounds."""
    if not isinstance(code, str):
        return False
    pattern = rf'^[A-Za-z0-9]{{{min_len},{max_len}}}$'
    return bool(re.fullmatch(pattern, code))

@app.post("/shorten")
def shorten():
    data = request.get_json() or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    url = url.strip()
    if not is_valid_url(url):
        return jsonify({"error": "Invalid URL format. Include http:// or https://"}), 400

    # Check if the URL already exists in the store
    for code, stored_url in _store.items():
        if stored_url == url:
            return jsonify({"code": code})  # Return the existing code

    # Generate a unique code
    code = generate_code()
    while code in _store:
        code = generate_code()

    # Store the mapping
    _store[code] = url
    return jsonify({"code": code})

@app.get("/<code>")
def resolve(code):
    # Validate code format before lookup
    if not is_valid_code(code):
        abort(400, description="Invalid code format")

    url = _store.get(code)
    if not url:
        abort(404, description="Code not found")
    return redirect(url)

@app.get("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

if __name__ == "__main__":
    app.run(port=8000)