"""
Streamer Mode - Advanced privacy and thematic masking for content creators.

Features:
- Replaces real file/folder names with 'creepy' aliases.
- Masks sensitive paths and network info.
- Disables invasive scares (like camera) if configured.
"""

import hashlib
import random
from config import Config
from core.logger import log_info

class StreamerMode:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StreamerMode, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized: return
        self.enabled = Config().get("STREAMER_MODE", False)
        self.mask_camera = Config().get("STREAMER_MASK_CAMERA", True)
        
        # Consistent mapping: real_name -> alias
        self._alias_map = {}
        self._horror_aliases = [
            "Kurban_Dosyası", "Ruh_Kaydı", "Gölge_Veri", "Unutulmuşlar", 
            "Feryat_Log", "Karanlık_Anılar", "Bozuk_Gerçeklik", "Sessiz_Çığlık",
            "Vasiyet", "Günahlar", "Korku_İlişki", "Son_Nefes"
        ]
        self._initialized = True
        log_info(f"Streamer Mode initialized. Enabled: {self.enabled}", "PRIVACY")

    def get_alias(self, original_name: str) -> str:
        """Returns a consistent horror alias for a real name."""
        if not self.enabled:
            return original_name
            
        if original_name in self._alias_map:
            return self._alias_map[original_name]
            
        # Deterministic choice based on hash
        name_hash = int(hashlib.md5(original_name.encode()).hexdigest(), 16)
        alias = self._horror_aliases[name_hash % len(self._horror_aliases)]
        
        # Add a unique suffix if collisions happen or to make it look 'technical'
        suffix = str(name_hash % 999).zfill(3)
        final_alias = f"{alias}_{suffix}"
        
        self._alias_map[original_name] = final_alias
        return final_alias

    def mask_path(self, path: str) -> str:
        """Masks a full file path."""
        if not self.enabled:
            return path
            
        parts = path.replace("\\", "/").split("/")
        masked_parts = []
        for p in parts:
            if not p or ":" in p: # Drive letter or empty
                masked_parts.append(p)
                continue
            masked_parts.append(self.get_alias(p))
            
        return "/".join(masked_parts)

    @staticmethod
    def singleton():
        return StreamerMode()
