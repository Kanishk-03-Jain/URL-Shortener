import qrcode
import io
import base64
from routes.shortener import URLShortener
class QRCodeGenerator:
    def __init__(self, url_shortener: URLShortener):
        self.url_shortener = url_shortener
    
    def generate_qr_code(self, url: str) -> str:
        """
        Generates a QR code for the shortened URL.
        
        Args:
            url (str): URL to generate a QR code for.
        
        Returns:
            str: The base64-encoded string of the generated QR code image.
        """

        if not url:
            raise ValueError("URL must not be empty")
        
        short_url = self.url_shortener.shorten_url(url)
        if not short_url:
            raise ValueError("Failed to generate short URL")
        
        img = qrcode.make(short_url)

        buf = io.BytesIO()
        img.save(buf, 'PNG')
        
        # Encode the image bytes to a Base64 string
        qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        return {
            "short_url": short_url,
            "qr_code_base64": qr_base64 
        }