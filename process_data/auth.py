# auth.py
import time
import bcrypt
import logging

logger = logging.getLogger(__name__)


class Authenticator:
    """
    Handles user authentication using secure bcrypt hashing.
    """

    def __init__(self, username: str = "admin", password: str = "12345"):
        """
        Initialize with provided or default credentials.

        Args:
            username: Username for login.
            password: Plain-text password (will be hashed internally).
        """
        self.username = username
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
        logger.info("Authenticator initialized for user: %s", self.username)

    def check_credentials(self, username: str, password: str) -> bool:
        """
        Verify credentials with brute-force protection delay.

        Returns:
            bool: True if credentials match.
        """
        if not username or not password:
            logger.warning("Login attempt with missing credentials")
            time.sleep(0.3)
            return False

        if username != self.username:
            logger.warning("Login attempt with incorrect username: %s", username)
            time.sleep(0.3)
            return False

        is_valid = bcrypt.checkpw(password.encode("utf-8"), self.password_hash)
        if is_valid:
            logger.info("Successful login for user: %s", username)
        else:
            logger.warning("Failed login attempt for user: %s", username)
            time.sleep(0.3)
        return is_valid