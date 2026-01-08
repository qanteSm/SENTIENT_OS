import os
import json
import zlib
import base64
import socket
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from config import Config

class SoulTransfer:
    """
    Handles the encryption and serialization of the AI's memory (Soul)
    into a proprietary '.echo' format for the USB Ritual.
    """
    HEADER = b"ECHO" # Magic Bytes

    def __init__(self, memory_data: dict):
        self.memory_data = memory_data
        self.key = self._generate_key()
        self.cipher = Fernet(self.key)

    def _generate_key(self):
        """Generates a key based on the Hostname (binding soul to this machine)."""
        hostname = socket.gethostname().encode()
        salt = b'SENTIENT_OS_V3_SALT' # Static salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(hostname))

    def create_vessel(self) -> bytes:
        """
        Creates the binary payload: HEADER + ENCRYPTED(COMPRESSED(JSON))
        """
        # 1. Serialize
        json_bytes = json.dumps(self.memory_data).encode('utf-8')
        
        # 2. Compress
        compressed = zlib.compress(json_bytes)
        
        # 3. Encrypt
        encrypted = self.cipher.encrypt(compressed)
        
        # 4. Pack
        return self.HEADER + encrypted

    def transfer_to_usb(self, drive_letter: str) -> bool:
        """Writes the .echo file to the USB drive root."""
        if Config.IS_MOCK:
            print(f"[SOUL] Mock Transfer to {drive_letter}:/SOUL.echo")
            return True

        try:
            filename = os.path.join(f"{drive_letter}:\\", "SOUL.echo")
            payload = self.create_vessel()
            
            with open(filename, 'wb') as f:
                f.write(payload)
                
            print(f"[SOUL] Transfer Complete: {filename}")
            return True
        except Exception as e:
            print(f"[SOUL] Transfer Failed: {e}")
            return False
