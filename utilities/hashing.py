import string
class Hasher:
    def __init__(self):
        self.CHARS = string.ascii_letters + string.digits
        self.BASE = len(self.CHARS)
    def get_unique_hash(self) -> str:
        """
        Generates a unique hash using the characters defined in CHARS.
        
        Returns:
            str: A unique hash string.
        """
        import random
        return ''.join(random.choices(self.CHARS, k=8))