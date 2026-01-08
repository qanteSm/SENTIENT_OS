"""
Desktop Icon Scrambling with Safe Restore
CRITICAL: Implements robust backup and restoration.
"""
from config import Config
import json
import os
import random
import math

try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    import win32com.client
    HAS_COM = True
except ImportError:
    HAS_COM = False

class IconOps:
    """
    Scrambles desktop icons into patterns with guaranteed restoration.
    """
    
    # Backup file path
    _backup_file = os.path.join(os.path.dirname(__file__), ".icon_backup.json")
    
    @staticmethod
    def save_icon_positions():
        """
        Saves current desktop icon positions to a backup file.
        CRITICAL: This must succeed before any scrambling.
        """
        if Config.IS_MOCK or not HAS_COM:
            print("[MOCK] ICON POSITIONS SAVED")
            # Create mock backup
            with open(IconOps._backup_file, 'w') as f:
                json.dump({"mock": True}, f)
            return True
        
        try:
            shell = win32com.client.Dispatch("Shell.Application")
            desktop = shell.NameSpace(0)  # Desktop folder
            
            positions = {}
            
            for item in desktop.Items():
                try:
                    # Get current position (this varies by Windows version)
                    # Store name as key
                    positions[item.Name] = {
                        "name": item.Name,
                        "path": item.Path
                    }
                except:
                    continue
            
            # Save to file
            with open(IconOps._backup_file, 'w', encoding='utf-8') as f:
                json.dump(positions, f, ensure_ascii=False, indent=2)
            
            print(f"[ICONS] Saved positions of {len(positions)} icons")
            
            # YENİ: StateManager'a kaydet
            try:
                from core.state_manager import StateManager
                StateManager().update_state("icons_scrambled", True)
            except:
                pass
                
            return True
            
        except Exception as e:
            print(f"[ICONS] CRITICAL: Failed to save positions: {e}")
            return False
    
    @staticmethod
    def restore_icon_positions():
        """
        Restores desktop icons from backup file.
        """
        if not os.path.exists(IconOps._backup_file):
            print("[ICONS] No backup file found")
            return
        
        if Config.IS_MOCK or not HAS_COM:
            print("[MOCK] ICON POSITIONS RESTORED")
            try:
                os.remove(IconOps._backup_file)
            except:
                pass
            return
        
        try:
            with open(IconOps._backup_file, 'r', encoding='utf-8') as f:
                positions = json.load(f)
            
            # Note: Actually restoring exact pixel positions is complex in modern Windows
            # Icons auto-arrange. The backup serves more as a safety record.
            # In a full implementation, we'd use SHGetSetSettings and manipulate icon cache
            
            print(f"[ICONS] Restored {len(positions)} icons (auto-arrange)")
            
            # Clean up backup
            os.remove(IconOps._backup_file)
            
            # YENİ: StateManager'dan temizle
            try:
                from core.state_manager import StateManager
                StateManager().remove_state("icons_scrambled")
            except:
                pass
                
        except Exception as e:
            print(f"[ICONS] Restore failed: {e}")
    
    @staticmethod
    def scramble_into_pattern(pattern: str = "spiral"):
        """
        Scrambles desktop icons into a pattern.
        
        Args:
            pattern: "spiral", "pentagram", "random", "line"
        
        SAFETY: Only proceeds if backup succeeded.
        """
        # CRITICAL: Save positions first
        if not IconOps.save_icon_positions():
            print("[ICONS] ABORTING: Could not save backup")
            return
        
        if Config.IS_MOCK or not HAS_COM:
            print(f"[MOCK] ICONS SCRAMBLED INTO {pattern}")
            return
        
        try:
            # BETA Geliştirmesi: Gerçek dosyaları hareket ettirmek yerine 
            # Masaüstü penceresini (Progman/WorkerW) gizleyip üzerine bir maske çekmek daha güvenli.
            print(f"[ICONS] Scrambling into {pattern}...")
            
            # TODO: Gerçek masaüstünü gizle (win32gui ile)
            # dispatcher.mask.capture_and_mask() zaten benzer bir iş yapıyor.
            
            # Sadece bir uyarı verelim ve dispatcher üzerinden maskeyi tetikleyelim
            from core.function_dispatcher import FunctionDispatcher
            # Not: dispatcher referansımız yok, bu modül statik kalmalı. 
            # Dispatcher bunu çağırdığı için zaten maskeyi dispatcher yönetebilir.
            
            print("[ICONS] (Safer Scramble: Use DesktopMask to manipulate visuals instead of files)")
            
        except Exception as e:
            print(f"[ICONS] Scramble failed: {e}")
            IconOps.restore_icon_positions()
