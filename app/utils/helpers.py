import random
import string
from urllib.parse import urlparse
from passlib.context import CryptContext

# Create a password context using bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes the given password using a secure hashing algorithm.
    """
    return pwd_context.hash(password)


def generate_random_string(length: int = 4) -> str:
    """
    Generates a random string of a specified length.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def extract_domain_from_url(company_website: str) -> str:
    """
    Extracts the domain name from the company website URL without the top-level domain (e.g., .com, .org).
    Handles both http and https URLs.
    """
    parsed_url = urlparse(company_website)

    # Remove 'www.' if it exists and extract the base domain
    domain = parsed_url.netloc.replace("www.", "").split(".")[0]

    # In case no domain is provided in the URL, fall back to the netloc
    if not domain:
        domain = parsed_url.path.split("/")[0]  # Handles edge cases like file paths

    return domain
