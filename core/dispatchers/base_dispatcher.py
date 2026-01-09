"""
Base Dispatcher Abstract Class

All specialized dispatchers inherit from this base class to ensure
consistent interface and behavior.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseDispatcher(ABC):
    """
    Abstract base class for all action dispatchers.
    
    Each specialized dispatcher (visual, hardware, horror, system) implements
    this interface to handle a specific category of actions.
    """
    
    @abstractmethod
    def get_supported_actions(self) -> List[str]:
        """
        Return list of action names this dispatcher handles.
        
        Returns:
            List of uppercase action names (e.g., ['OVERLAY_TEXT', 'FLASH_COLOR'])
        """
        pass
    
    @abstractmethod
    def dispatch(self, action: str, params: Dict[str, Any], speech: str = ""):
        """
        Execute the given action with parameters.
        
        Args:
            action: The action name (uppercase)
            params: Dictionary of action parameters
            speech: Optional speech text for TTS
            
        Raises:
            DispatchError: If action execution fails
        """
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}(actions={len(self.get_supported_actions())})"
