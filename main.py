from flask import Flask, request, jsonify
from flask_cors import CORS
from services.databaseServices import DatabaseService
from routes.shortener import URLShortener
from utilities.hashing import Hasher
import logging
app = Flask(__name__)
CORS(app)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database_service = DatabaseService()
hasher = Hasher()
url_shortener = URLShortener(hasher, database_service)

@app.route('/', methods=['GET']) 
def index():
    BASE_URL = request.base_url
    return jsonify({"message": "Welcome to the URL Shortener API"}), 200

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    Shortens a given URL.
    Args:
        url (str): The original URL to shorten.
    Returns:
        dict: A dictionary containing the short URL.
    """
    data = request.get_json()
    base_url = request.base_url[:-len('/shorten')]
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    existing_hash = database_service.get_existing_hash(url)
    if existing_hash:
        short_url = f"{base_url}/{existing_hash}"
        logger.info(f"URL already exists, returning existing short URL: {short_url}")
        return jsonify({"short_url": short_url}), 200
    hash = url_shortener.get_url_hash(url)
    if not hash:
        return jsonify({"error": "Failed to shorten hash"}), 500
    short_url = f"{base_url}/{hash}"
    logger.info(f"Shortened URL: {short_url} for original URL: {url}")
    
    database_service.store_hash(url, hash)

    return jsonify({"short_url": short_url}), 201

@app.route('/<hash>', methods=['GET'])
def redirect(hash):
    """
    Redirects to the original URL based on the provided short URL.
    Args:
        short_url (str): The short URL to redirect from.
    Returns:
        str: The original URL to redirect to.
    Raises:
        ValueError: If the short URL is not found in the database.
    """
    if not hash:
        return jsonify({"error": "Short URL is required"}), 400

    original_url = database_service.get_original_url(hash)
    if not original_url:
        return jsonify({"error": "Short URL not found"}), 404
    
    logger.info(f"Redirecting to: {original_url}")
    return jsonify({"original_url": original_url}), 302

app.run(debug=True, host='0.0.0.0', port=5000)