# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import json
import os
from config import Config

class LocalizationManager:
    """
    Manages loading and serving localized strings.
    Singleton pattern.
    """
    _instance = None
    _strings = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalizationManager, cls).__new__(cls)
            cls._instance.load_locale()
        return cls._instance

    def load_locale(self):
        """Loads the JSON file for the configured language."""
        lang_code = Config().get("LANGUAGE", "tr") 
        path = os.path.join(Config().LOCALES_DIR, f"{lang_code}.json")
        
        if not os.path.exists(path):
            print(f"[LOCALE] Warning: Locale file {path} not found. Fallback to 'tr'.")
            path = os.path.join(Config().LOCALES_DIR, "tr.json")
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._strings = json.load(f)
            print(f"[LOCALE] Loaded {lang_code} successfully.")
        except Exception as e:
            print(f"[LOCALE] Failed to load locale: {e}")
            self._strings = {}

    def get(self, key: str, default: str = None) -> str:
        """
        Retrieves a string by key. Supports nested keys like 'category.key'.
        """
        keys = key.split('.')
        val = self._strings
        
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default or key

# Global instance helper
def tr(key: str, default: str = None) -> str:
    return LocalizationManager().get(key, default)
