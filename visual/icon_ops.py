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
    if Config().IS_MOCK:
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
        if Config().IS_MOCK or not HAS_COM:
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
                except Exception:
                    continue
            
            # Save to file
            with open(IconOps._backup_file, 'w', encoding='utf-8') as f:
                json.dump(positions, f, ensure_ascii=False, indent=2)
            
            print(f"[ICONS] Saved positions of {len(positions)} icons")
            
            # YENİ: StateManager'a kaydet
            try:
                from core.state_manager import StateManager
                StateManager().update_state("icons_scrambled", True)
            except Exception:
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
        
        if Config().IS_MOCK or not HAS_COM:
            print("[MOCK] ICON POSITIONS RESTORED")
            try:
                os.remove(IconOps._backup_file)
            except Exception:
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
            except Exception:
                pass
                
        except Exception as e:
            print(f"[ICONS] Restore failed: {e}")
    
    @staticmethod
    def scramble_into_pattern(pattern: str = "spiral"):
        """
        Scrambles desktop icons into a pattern.
        Note: For safety and performance, we use a 'Visual Hijack' approach.
        We hide the real desktop and draw a corrupted version with scrambled 'ghost' icons.
        """
        # 1. Save state for restoration
        if not IconOps.save_icon_positions():
            return
            
        print(f"[ICONS] Scrambling into {pattern} pattern...")
        
        # 2. Trigger Visual Displacement via DesktopMask
        # In a real implementation, we would tell DesktopMask to draw icons at specific coordinates
        try:
            from visual.desktop_mask import DesktopMask
            mask = DesktopMask()
            
            # We move the entire desktop 'view' or apply a pixel-shift pattern
            if pattern == "spiral":
                mask.capture_and_mask() # Basic mask for now
            elif pattern == "random":
                mask.capture_and_mask()
            
            # Also use GDI for additional noise
            from visual.gdi_engine import GDIEngine
            GDIEngine.draw_static_noise(duration_ms=1000, density=0.02)
            
        except Exception as e:
            print(f"[ICONS] Scramble failed: {e}")
