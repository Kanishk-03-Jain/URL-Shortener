from services.databaseServices import DatabaseService
from utilities.hashing import Hasher
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
        

    