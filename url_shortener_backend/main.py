from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from services.databaseServices import DatabaseService
from routes.shortener import URLShortener
from utilities.hashing import Hasher
import logging
import re
from urllib.parse import urlparse
import config
app = Flask(__name__)
# app.config['SECRET_KEY'] = config.SECRET_KEY
CORS(app)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database_service = DatabaseService()
hasher = Hasher()
url_shortener = URLShortener(hasher, database_service)

def is_valid_url(url):
    """Simple URL validation function."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except:
        return False

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
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Basic URL validation
    if not is_valid_url(url):
        return jsonify({"error": "Invalid URL format"}), 400
    
    # Check URL length (prevent extremely long URLs)
    if len(url) > config.MAX_URL_LENGTH:
        return jsonify({"error": f"URL too long (max {config.MAX_URL_LENGTH} characters)"}), 400
    
    try:
        existing_hash = database_service.get_existing_hash(url)
        if existing_hash:
            base_url = request.base_url[:-len('/shorten')]
            short_url = f"{base_url}/{existing_hash}"
            logger.info(f"URL already exists, returning existing short URL")
            return jsonify({"short_url": short_url}), 200
        
        hash = url_shortener.get_url_hash(url)
        if not hash:
            return jsonify({"error": "Failed to generate hash"}), 500
        
        database_service.store_hash(url, hash)
        
        base_url = request.base_url[:-len('/shorten')]
        short_url = f"{base_url}/{hash}"
        logger.info(f"Created short URL for original URL")
        
        return jsonify({"short_url": short_url}), 201
    except Exception as e:
        logger.error(f"Error shortening URL: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/<hash>', methods=['GET'])
def redirect_to_original(hash):
    """
    Redirects to the original URL based on the provided short URL.
    Args:
        hash (str): The hash from the short URL.
    Returns:
        str: The original URL to redirect to.
    Raises:
        ValueError: If the short URL is not found in the database.
    """
    if not hash or not hash.strip():
        return jsonify({"error": "Hash is required"}), 400
    
    # Basic validation of hash format
    if not re.match(r'^[a-zA-Z0-9]+$', hash) or len(hash) != config.HASH_LENGTH:
        return jsonify({"error": "Invalid hash format"}), 400

    try:
        original_url = database_service.get_original_url(hash)
        if not original_url:
            return jsonify({"error": "Short URL not found"}), 404
        
        logger.info(f"Redirecting hash {hash} to original URL {original_url}")
        original_url = original_url.strip()
        return redirect(original_url, code=302)
        # return jsonify({"original_url": original_url}), 302
    except Exception as e:
        logger.error(f"Error during redirect: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)