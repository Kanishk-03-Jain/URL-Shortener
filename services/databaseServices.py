import psycopg2
from psycopg2 import sql
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import os
import json
import uuid
from datetime import date
import pytz
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv

class DatabaseService:
    def __init__(self):
        """
        Initialize database service with configuration from environment variables
        """
        # Load environment variables
        load_dotenv()
        
        # Get database configuration from environment variables
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT')),
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        # Initialize logger
        self.logger = logger
        
    def _get_connection(self):
        """
        Create a database connection
        
        Returns:
            psycopg2.connection: Database connection
        """
        try:
            conn = psycopg2.connect(**self.db_config)
            self.logger.info(" Successfully connected to RDS PostgreSQL database")
            return conn
        except Exception as e:
            self.logger.error(f" Failed to connect to database: {str(e)}", exc_info=True)
            raise
    
    def store_hash(self, original_url: str, hash: str) -> None:
        """
        Store the original and hash in the database
        
        Args:
            original_url (str): The original URL to store
            hash (str): The shortened URL to store
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            insert_query = sql.SQL("""
                INSERT INTO urls (hash, url, created_at)
                VALUES (%s, %s, %s)
            """)
            cursor.execute(insert_query, (hash, original_url, datetime.now()))
            
            conn.commit()
            cursor.close()
            conn.close()
            self.logger.info(f"Stored URL: {original_url} as {hash}")
        except Exception as e:
            self.logger.error(f"Failed to store URL: {str(e)}", exc_info=True)
            raise
    def get_original_url(self, hash: str) -> Optional[str]:
        """
        Retrieve the original URL based on the short URL
        
        Args:
            short_url (str): The shortened URL to look up
        
        Returns:
            Optional[str]: The original URL if found, None otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            select_query = sql.SQL("""
                SELECT url FROM urls WHERE hash = %s
            """)
            cursor.execute(select_query, (hash,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                self.logger.info(f"Found original URL: {result[0]} for short URL: {hash}")
                return result[0]
            else:
                self.logger.warning(f"No original URL found for short URL: {hash}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to retrieve original URL: {str(e)}", exc_info=True)
            raise

    def get_existing_hash(self, url: str) -> Optional[str]:
        """
        Check if a hash for the given URL already exists in the database
        
        Args:
            url (str): The original URL to check
        
        Returns:
            Optional[str]: The existing hash if found, None otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            select_query = sql.SQL("""
                SELECT hash FROM urls WHERE url = %s
            """)
            cursor.execute(select_query, (url,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                self.logger.info(f"Found existing hash: {result[0]} for URL: {url}")
                return result[0]
            else:
                self.logger.warning(f"No existing hash found for URL: {url}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to check existing hash: {str(e)}", exc_info=True)
            raise

    def check_hash_exists(self, hash_value: str) -> bool:
        """
        Check if a hash already exists in the database
        
        Args:
            hash_value (str): The hash to check
        
        Returns:
            bool: True if the hash exists, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            select_query = sql.SQL("""
                SELECT EXISTS(SELECT 1 FROM urls WHERE hash = %s)
            """)
            cursor.execute(select_query, (hash_value,))
            exists = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            self.logger.info(f"Hash {hash_value} exists: {exists}")
            return exists
        except Exception as e:
            self.logger.error(f"Failed to check if hash exists: {str(e)}", exc_info=True)
            raise
