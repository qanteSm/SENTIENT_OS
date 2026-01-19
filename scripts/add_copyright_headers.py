# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# =========================================================================
"""
Script to add copyright headers to all Python files in the project.
Run this script to ensure all .py files have proper copyright protection.

Usage: python scripts/add_copyright_headers.py
"""

import os
from pathlib import Path

COPYRIGHT_HEADER = '''# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

'''

SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.env'}
SKIP_FILES = {'__init__.py'}  # These often have special imports at top

def has_copyright_header(content: str) -> bool:
    """Check if file already has our copyright header"""
    return "Copyright (c) 2026 Muhammet Ali Büyük" in content

def add_header_to_file(filepath: Path) -> bool:
    """Add copyright header to a Python file. Returns True if modified."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if has_copyright_header(content):
            return False  # Already has header
        
        # Add header at the beginning
        new_content = COPYRIGHT_HEADER + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Get project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent
    
    modified_count = 0
    skipped_count = 0
    error_count = 0
    
    print(f"Adding copyright headers to Python files in: {project_root}")
    print("-" * 60)
    
    for root, dirs, files in os.walk(project_root):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            if not file.endswith('.py'):
                continue
            
            filepath = Path(root) / file
            
            if add_header_to_file(filepath):
                print(f"✓ Added header: {filepath.relative_to(project_root)}")
                modified_count += 1
            else:
                skipped_count += 1
    
    print("-" * 60)
    print(f"Summary:")
    print(f"  Modified: {modified_count} files")
    print(f"  Skipped (already has header): {skipped_count} files")
    print(f"  Errors: {error_count} files")

if __name__ == "__main__":
    main()
