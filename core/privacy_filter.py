import re
import os
import getpass

class PrivacyFilter:
    """
    Scrubs sensitive information from strings before they are sent to the AI.
    Focuses on: Usernames, Home Directories, IP Addresses, and sensitive system paths.
    """
    def __init__(self):
        self.username = getpass.getuser()
        self.patterns = [
            # 1. Scrub actual username
            (re.compile(re.escape(self.username), re.IGNORECASE), "<USER>"),
            
            # 2. Scrub Windows Path artifacts
            (re.compile(r'[a-zA-Z]:\\Users\\[^\s\\]+', re.IGNORECASE), "<USER_DIR>"),
            
            # 3. Scrub IP Addresses (v4)
            (re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'), "<IP_ADDR>"),
            
            # 4. Scrub common sensitive paths
            (re.compile(r'C:\\(Windows|Program Files|System32)', re.IGNORECASE), "<SYS_PATH>")
        ]

    def scrub(self, text: str) -> str:
        """Applies all regex patterns to scrub the text."""
        if not text:
            return ""
            
        scrubbed = text
        for pattern, replacement in self.patterns:
            scrubbed = pattern.sub(replacement, scrubbed)
            
        return scrubbed

    @staticmethod
    def singleton():
        if not hasattr(PrivacyFilter, "_instance"):
            PrivacyFilter._instance = PrivacyFilter()
        return PrivacyFilter._instance
