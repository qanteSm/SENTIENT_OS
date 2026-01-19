# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Quick fix script to replace Config().IS_MOCK, Config().IS_WINDOWS etc. 
with Config().IS_MOCK, Config().IS_WINDOWS across all files.
"""

import os
import re

def fix_config_access(file_path):
    """Fix static Config access to instance access"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Replace Config.ATTRIBUTE with Config().ATTRIBUTE
        # But NOT Config._internal_attributes
        patterns = [
            (r'\bConfig\.IS_MOCK\b', 'Config().IS_MOCK'),
            (r'\bConfig\.IS_WINDOWS\b', 'Config().IS_WINDOWS'),
            (r'\bConfig\.BASE_DIR\b', 'Config().BASE_DIR'),
            (r'\bConfig\.LOCALES_DIR\b', 'Config().LOCALES_DIR'),
            (r'\bConfig\.LOGS_DIR\b', 'Config().LOGS_DIR'),
            (r'\bConfig\.CACHE_DIR\b', 'Config().CACHE_DIR'),
            (r'\bConfig\.ASSETS_DIR\b', 'Config().ASSETS_DIR'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"✗ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all Python files in sentient_os directory"""
    base_dir = r"c:\Users\Betül Büyük\Downloads\megasentito\v8\sentient_os"
    
    count = 0
    for root, dirs, files in os.walk(base_dir):
        # Skip venv and cache directories
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_config_access(file_path):
                    count += 1
    
    print(f"\n✓ Fixed {count} files")

if __name__ == "__main__":
    main()
