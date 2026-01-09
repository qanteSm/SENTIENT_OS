from config import Config

class ProcessGuard:
    """
    Ensures the AI does not interact with or kill protected processes (OBS, Discord, etc.).
    This is critical for Streamer Mode.
    """
    def __init__(self):
        self.protected_list = Config().get("PROTECTED_PROCESSES", [])

    def is_protected(self, process_name: str) -> bool:
        """Checks if a process is in the whitelist."""
        return process_name.lower() in self.protected_list

    def filter_action(self, target_process: str, action_type: str) -> bool:
        """
        Returns True if the action is ALLOWED.
        Returns False if the action is BLOCKED because the target is protected.
        """
        if self.is_protected(target_process):
            # Log violation attempt
            return False
        return True
