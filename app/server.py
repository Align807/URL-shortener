# filepath: c:\Users\align\Downloads\02-ambiguous-url-shortener\02-ambiguous-url-shortener\app\server.py
from flask import Flask, request, jsonify, redirect, abort, send_from_directory
import random
import string
import os

app = Flask(__name__)

# In-memory store for URL mappings
_store = {}

def generate_code(length=6):
    """Generate a random short code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten")
def shorten():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

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
    url = _store.get(code)
    if not url:
        abort(404, description="Code not found")
    return redirect(url)

@app.get("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

if __name__ == "__main__":
    app.run(port=8000)