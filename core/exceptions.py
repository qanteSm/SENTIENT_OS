"""
Custom Exceptions for SENTIENT_OS

Provides a hierarchy of specific exceptions for better error handling
and debugging throughout the application.
"""


class SentientError(Exception):
    """
    Base exception for all SENTIENT_OS errors.
    
    All custom exceptions should inherit from this class.
    Includes optional details dictionary for additional context.
    """
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class AIResponseError(SentientError):
    """
    AI returned invalid, malformed, or unparseable response.
    
    Examples:
    - Invalid JSON format
    - Missing required fields
    - Unexpected response structure
    """
    pass


class HardwareAccessError(SentientError):
    """
    Failed to access or control hardware device.
    
    Examples:
    - Mouse/keyboard control failed
    - Camera not accessible
    - Audio device unavailable
    - Display/monitor operation failed
    """
    pass


class APIConnectionError(SentientError):
    """
    Failed to connect to external API.
    
    Examples:
    - Gemini API connection timeout
    - Network unavailable
    - API key invalid
    - Rate limit exceeded
    """
    pass


class ConfigurationError(SentientError):
    """
    Invalid configuration detected.
    
    Examples:
    - Missing required config value
    - Invalid config value type
    - YAML parsing error
    - Config file not found
    """
    pass


class ValidationError(SentientError):
    """
    Input validation failed.
    
    Examples:
    - AI response validation failed
    - Config value validation failed
    - User input validation failed
    """
    pass


class StoryStateError(SentientError):
    """
    Story/Act state inconsistency or error.
    
    Examples:
    - Invalid Act transition
    - Missing story checkpoint
    - Corrupted save state
    """
    pass


class MemoryError(SentientError):
    """
    Memory system error.
    
    Examples:
    - Failed to load memory
    - Failed to save memory
    - Corrupted memory data
    """
    pass


class DispatchError(SentientError):
    """
    Function dispatcher error.
    
    Examples:
    - Unknown action
    - Missing required parameters
    - Action execution failed
    """
    pass
