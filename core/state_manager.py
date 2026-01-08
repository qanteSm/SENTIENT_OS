import os
import json
import time
from config import Config
from core.logger import log_info, log_error, log_warning

class StateManager:
    """
    Central registry for system modifications. 
    Ensures that if the game crashes, the system is restored to its original state on the next boot.
    """
    _instance = None
    _state_file = os.path.join(Config.BASE_DIR, ".system_state.json")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance.data = {}
            cls._instance.load_state()
        return cls._instance

    def load_state(self):
        """Loads state from file."""
        try:
            if os.path.exists(self._state_file):
                with open(self._state_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                log_info("System state loaded.", "STATE")
        except Exception as e:
            log_error(f"Failed to load state: {e}", "STATE")
            self.data = {}

    def save_state(self):
        """Saves current state to file."""
        try:
            with open(self._state_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            log_error(f"Failed to save state: {e}", "STATE")

    def update_state(self, key, value):
        """Updates a state entry and saves it."""
        self.data[key] = {
            "value": value,
            "timestamp": time.time()
        }
        self.save_state()

    def get_state(self, key):
        """Retrieves a state entry."""
        entry = self.data.get(key)
        return entry.get("value") if entry else None

    def remove_state(self, key):
        """Removes a state entry and saves."""
        if key in self.data:
            del self.data[key]
            self.save_state()

    def clear_all(self):
        """Clears the state file."""
        self.data = {}
        if os.path.exists(self._state_file):
            try:
                os.remove(self._state_file)
                log_info("System state cleared successfully.", "STATE")
            except:
                pass

    def check_for_recovery(self, dispatcher) -> bool:
        """
        FIXED: Checks if there are pending modifications that need restoration.
        Returns True if recovery was performed.
        """
        if not self.data:
            return False

        log_warning("Recovery data found! Restoring system state...", "STATE")
        
        # Dispatch restoration actions
        dispatcher.dispatch({"action": "RESTORE_SYSTEM"})
        
        # After restoration, clear the state
        self.clear_all()
        return True
