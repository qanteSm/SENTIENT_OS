# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Checkpoint Manager - Save/Load sistem iyileştirmesi
Act başlarında checkpoint oluşturur, crash recovery için kullanılır.
"""
import os
import json
import time
import shutil
from config import Config
from core.logger import log_info, log_error, log_warning

class CheckpointManager:
    """
    Manages game checkpoints for crash recovery and save/load.
    """
    
    def __init__(self, memory):
        self.memory = memory
        
        # Checkpoint directory
        if Config().IS_WINDOWS:
            app_data = os.getenv('APPDATA')
            self.checkpoint_dir = os.path.join(app_data, "SentientOS", "checkpoints")
        else:
            self.checkpoint_dir = os.path.join(Config().BASE_DIR, "checkpoints")
        
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        self.max_checkpoints = 5  # Keep last 5 checkpoints
    
    def create(self, name: str):
        """
        Creates a checkpoint with the given name.
        
        Args:
            name: Checkpoint identifier (e.g., "act_1_start", "act_2_mid")
        """
        timestamp = int(time.time())
        filename = f"cp_{timestamp}_{name}.json"
        filepath = os.path.join(self.checkpoint_dir, filename)
        
        # Create checkpoint data
        checkpoint_data = {
            "_checkpoint_meta": {
                "name": name,
                "timestamp": timestamp,
                "version": Config().get("VERSION", "0.8.0"),
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "data": self.memory.data.copy()
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
            
            log_info(f"Created: {name} at {filepath}", "CHECKPOINT")
            
            # Cleanup old checkpoints
            self._cleanup_old()
            
            return True
        except Exception as e:
            log_error(f"Failed to create: {e}", "CHECKPOINT")
            return False
    
    def get_latest(self):
        """Returns the latest checkpoint data, or None if none exist."""
        checkpoints = self._list_checkpoints()
        if not checkpoints:
            return None
        
        # Get the most recent one
        latest = checkpoints[-1]
        
        try:
            with open(latest["path"], 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log_error(f"Failed to load latest: {e}", "CHECKPOINT")
            return None
    
    def restore_latest(self):
        """
        Restores from the latest checkpoint.
        Returns True if successful, False otherwise.
        """
        checkpoint = self.get_latest()
        if not checkpoint:
            log_warning("No checkpoints found to restore", "CHECKPOINT")
            return False
        
        try:
            self.memory.data = checkpoint["data"]
            meta = checkpoint.get("_checkpoint_meta", {})
            log_info(f"Restored from: {meta.get('name', 'unknown')}", "CHECKPOINT")
            return True
        except Exception as e:
            log_error(f"Restore failed: {e}", "CHECKPOINT")
            return False
    
    def _list_checkpoints(self):
        """Lists all checkpoints sorted by timestamp."""
        checkpoints = []
        
        try:
            for filename in os.listdir(self.checkpoint_dir):
                if filename.startswith("cp_") and filename.endswith(".json"):
                    filepath = os.path.join(self.checkpoint_dir, filename)
                    
                    # Parse timestamp from filename
                    parts = filename.replace(".json", "").split("_")
                    if len(parts) >= 2:
                        try:
                            timestamp = int(parts[1])
                            name = "_".join(parts[2:]) if len(parts) > 2 else "unknown"
                            checkpoints.append({
                                "path": filepath,
                                "timestamp": timestamp,
                                "name": name
                            })
                        except ValueError:
                            pass
            
            checkpoints.sort(key=lambda x: x["timestamp"])
            
        except Exception as e:
            log_error(f"Failed to list: {e}", "CHECKPOINT")
        
        return checkpoints
    
    def _cleanup_old(self):
        """Removes old checkpoints, keeping only the most recent ones."""
        checkpoints = self._list_checkpoints()
        
        if len(checkpoints) > self.max_checkpoints:
            to_remove = checkpoints[:-self.max_checkpoints]
            
            for cp in to_remove:
                try:
                    os.remove(cp["path"])
                    log_info(f"Cleaned up old: {cp['name']}", "CHECKPOINT")
                except (OSError, PermissionError) as e:
                    log_error(f"Failed to remove {cp['name']}: {e}", "CHECKPOINT")
                    pass
    
    def has_checkpoints(self):
        """Returns True if any checkpoints exist."""
        return len(self._list_checkpoints()) > 0
    
    def get_checkpoint_info(self):
        """Returns info about available checkpoints for UI display."""
        checkpoints = self._list_checkpoints()
        
        if not checkpoints:
            return None
        
        latest = checkpoints[-1]
        return {
            "count": len(checkpoints),
            "latest_name": latest["name"],
            "latest_time": time.strftime("%Y-%m-%d %H:%M:%S", 
                                         time.localtime(latest["timestamp"]))
        }
