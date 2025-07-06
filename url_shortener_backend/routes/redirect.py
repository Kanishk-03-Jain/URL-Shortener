def redirect_to_url(short_url):
    """
    Redirects to the original URL based on the provided short URL.
    Args:
        short_url (str): The short URL to redirect from.
    Returns:
        str: The original URL to redirect to.
    Raises:
        ValueError: If the short URL is not found in the database.
    """

    