from services.databaseServices import DatabaseService
from utilities.hashing import Hasher
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class URLShortener:
    def __init__(self, hasher: Hasher, database_service: DatabaseService):
        """
        Initialize URLShortener with a hasher and database service.
        
        Args:
            hasher: An instance of a hashing utility.
            database_service: An instance of a database service for storing URLs.
        """
        self.hasher = hasher
        self.database_service = database_service
    
    def get_url_hash(self, original_url: str) -> str:
        """
        Shortens a given URL.
        
        Args:
            original_url (str): The original URL to shorten.
        
        Returns:
            str: A shortened URL.
        """
        existing_hash = self.database_service.get_existing_hash(original_url)
        if existing_hash:
            return existing_hash
        
        unique_hash = self.hasher.get_unique_hash()
        while self.database_service.check_hash_exists(unique_hash):
            unique_hash = self.hasher.get_unique_hash()
        
        return unique_hash
        

    def shorten_url(self, original_url: str, base_url: str) -> str:
        """
        Shortens a given URL and stores it in the database.
        
        Args:
            original_url (str): The original URL to shorten.
            base_url (str): The base URL for the shortened URL.
        
        Returns:
            str: The shortened URL.
        """
        if not original_url:
            raise ValueError("Original URL must not be empty")
        
        try:
            existing_hash = self.database_service.get_existing_hash(original_url)
            if existing_hash:
                short_url = f"{base_url}/{existing_hash}"
                logger.info(f"URL already exists, returning existing short URL")
                return short_url

            hash = self.get_url_hash(original_url)
            if not hash:
                return None

            self.database_service.store_hash(original_url, hash)

            short_url = f"{base_url}/{hash}"
            logger.info(f"Created short URL for original URL")

            return short_url
        except Exception as e:
            logger.error(f"Error shortening URL: {str(e)}")
            return None