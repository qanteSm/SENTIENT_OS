"""
File System Awareness - Safe desktop folder scanning.

Provides AI with context about user's desktop folders
WITHOUT reading file contents (privacy-safe).

SAFETY:
- Read-only operations
- Folder names only (no contents)
- Limited to Desktop directory
- Respects privacy settings
"""

import os
from typing import List
from pathlib import Path


class FileSystemAwareness:
    """
    Safe file system observation for AI context.
    
    CRITICAL SAFETY:
    - NEVER reads file contents
    - NEVER modifies files
    - Only lists folder/file NAMES
    - Limited to specific safe directories
    """
    
    @staticmethod
    def get_desktop_folders(max_count=5) -> List[str]:
        """
        Get desktop folder names (not contents).
        
        Args:
            max_count: Maximum folders to return
            
        Returns:
            List of folder names
        """
        try:
            desktop = Path.home() / "Desktop"
            
            if not desktop.exists():
                return []
            
            # List directories only
            folders = [
                item.name for item in desktop.iterdir()
                if item.is_dir() and not item.name.startswith('.')
            ]
            
            # Limit count
            return folders[:max_count]
            
        except Exception as e:
            print(f"[FILE_AWARENESS] Error reading desktop: {e}")
            return []
    
    @staticmethod
    def get_desktop_file_names(max_count=10) -> List[str]:
        """
        Get desktop file names (not contents).
        
        Args:
            max_count: Maximum files to return
            
        Returns:
            List of file names (without extensions for privacy)
        """
        try:
            desktop = Path.home() / "Desktop"
            
            if not desktop.exists():
                return []
            
            # List files only
            files = [
                item.stem for item in desktop.iterdir()  # stem = name without extension
                if item.is_file() and not item.name.startswith('.')
            ]
            
            # Filter out sensitive files
            sensitive_keywords = ['password', 'key', 'secret', 'private', 'credential']
            files = [
                f for f in files
                if not any(keyword in f.lower() for keyword in sensitive_keywords)
            ]
            
            return files[:max_count]
            
        except Exception as e:
            print(f"[FILE_AWARENESS] Error reading files: {e}")
            return []
    
    @staticmethod
    def get_context_for_ai() -> dict:
        """
        Get safe file system context for AI.
        
        Returns:
            Dictionary with folder/file information
        """
        from config import Config
        
        # Check if enabled
        config = Config()
        if config.get("STREAMER_MODE", True):
            # In streamer mode, very limited info
            return {
                "desktop_folders": [],
                "desktop_files": []
            }
        
        return {
            "desktop_folders": FileSystemAwareness.get_desktop_folders(),
            "desktop_files": FileSystemAwareness.get_desktop_file_names()
        }
    
    @staticmethod
    def generate_ai_prompt_addon() -> str:
        """
        Generate AI prompt addition with file system context.
        
        Returns:
            String to add to AI prompt
        """
        context = FileSystemAwareness.get_context_for_ai()
        
        folders = context.get("desktop_folders", [])
        files = context.get("desktop_files", [])
        
        if not folders and not files:
            return ""
        
        prompt_addon = "\n=== DESKTOP OBSERVATION ===\n"
        
        if folders:
            prompt_addon += f"Klasörler: {', '.join(folders)}\n"
            prompt_addon += "UYARI: Bu klasörlerin İSİMLERİNİ tehdit için kullanabilirsin, ama ASLA silme!\n"
        
        if files:
            prompt_addon += f"Dosyalar: {', '.join(files[:5])}\n"
            prompt_addon += "Örnek: 'Tatil Fotoğrafları klasörünü silmemi ister misin?'\n"
        
        return prompt_addon
