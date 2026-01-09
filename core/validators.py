"""
Input Validation Module for SENTIENT_OS

Provides validation functions for AI responses, configuration values,
and other critical inputs to prevent errors and improve security.
"""
from typing import Dict, Any, List
from core.exceptions import ValidationError


# Valid action types that the AI can return
VALID_ACTIONS = [
    # No action
    "NONE",
    
    # Visual effects
    "OVERLAY_TEXT",
    "SCREEN_TEAR",
    "PIXEL_MELT",
    "FAKE_BSOD",
    "FLASH_SCREEN",
    "WALLPAPER_CHANGE",
    "BRIGHTNESS_FLICKER",
    "THE_MASK",
    "GLITCH_DESKTOP",
    "FAKE_ERROR",
    "FAKE_VIRUS_SCAN",
    
    # Hardware control
    "MOUSE_SHAKE",
    "MOUSE_TELEPORT",
    "KEYBOARD_BLOCK",
    "KEYBOARD_SPAM",
    "CAMERA_FLASH",
    "CAMERA_SNAPSHOT",
    
    # Audio
    "TTS_SPEAK",
    "DRONE_CHANGE",
    "PLAY_SOUND",
    
    # System operations
    "NOTIFICATION_SEND",
    "CLIPBOARD_INJECT",
    "WINDOW_MANIPULATE",
    "NOTEPAD_SPAWN",
    "FAKE_FILE_DELETE",
    "FAKE_BROWSER_HISTORY",
    
    # Story progression
    "PROGRESS_STORY",
    "CHANGE_ACT",
    
    # Special
    "EXORCISM_START",
    "RITUAL_CHECK",
]


def validate_ai_response(response: Dict[str, Any]) -> bool:
    """
    Validate AI response structure and content.
    
    Expected format:
    {
        "action": str (must be in VALID_ACTIONS),
        "params": dict (optional),
        "speech": str (optional)
    }
    
    Args:
        response: The AI response dictionary to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If response is invalid
    """
    # Check if response is a dictionary
    if not isinstance(response, dict):
        raise ValidationError(
            "Response must be a dictionary",
            details={"received_type": type(response).__name__}
        )
    
    # Required field: action
    if "action" not in response:
        raise ValidationError(
            "Missing required field: action",
            details={"response": response}
        )
    
    action = response["action"]
    
    # Validate action type
    if not isinstance(action, str):
        raise ValidationError(
            "Action must be a string",
            details={"action": action, "type": type(action).__name__}
        )
    
    # Validate action is in allowed list
    if action not in VALID_ACTIONS:
        raise ValidationError(
            f"Invalid action: {action}",
            details={
                "action": action,
                "valid_actions": VALID_ACTIONS
            }
        )
    
    # Optional field: params
    if "params" in response:
        params = response["params"]
        if not isinstance(params, dict):
            raise ValidationError(
                "params must be a dictionary",
                details={"params": params, "type": type(params).__name__}
            )
    
    # Optional field: speech
    if "speech" in response:
        speech = response["speech"]
        if not isinstance(speech, str):
            raise ValidationError(
                "speech must be a string",
                details={"speech": speech, "type": type(speech).__name__}
            )
    
    return True


def validate_config_value(key: str, value: Any) -> bool:
    """
    Validate configuration values based on key type.
    
    Args:
        key: Configuration key name
        value: Value to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If value is invalid for the given key
    """
    validators = {
        "CHAOS_LEVEL": lambda v: isinstance(v, (int, float)) and 0 <= v <= 100,
        "LANGUAGE": lambda v: isinstance(v, str) and v in ["tr", "en"],
        "TARGET_MONITOR_INDEX": lambda v: isinstance(v, int) and v >= 0,
        "STREAMER_MODE": lambda v: isinstance(v, bool),
        "AI_SAFETY_CHECK": lambda v: isinstance(v, bool),
        "SAFE_HARDWARE": lambda v: isinstance(v, bool),
        "ENABLE_STROBE": lambda v: isinstance(v, bool),
    }
    
    if key in validators:
        if not validators[key](value):
            raise ValidationError(
                f"Invalid value for {key}",
                details={"key": key, "value": value}
            )
    
    return True


def validate_action_params(action: str, params: Dict[str, Any]) -> bool:
    """
    Validate parameters for specific actions.
    
    Args:
        action: The action name
        params: Parameters dictionary
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If parameters are invalid
    """
    # Define required/optional parameters for each action
    param_requirements = {
        "OVERLAY_TEXT": {
            "required": ["text"],
            "optional": ["duration", "color", "size"]
        },
        "TTS_SPEAK": {
            "required": ["text"],
            "optional": ["rate", "volume"]
        },
        "MOUSE_SHAKE": {
            "required": [],
            "optional": ["intensity", "duration"]
        },
        "NOTIFICATION_SEND": {
            "required": ["title", "message"],
            "optional": ["duration"]
        }
    }
    
    if action in param_requirements:
        requirements = param_requirements[action]
        
        # Check required parameters
        for required_param in requirements["required"]:
            if required_param not in params:
                raise ValidationError(
                    f"Missing required parameter for {action}: {required_param}",
                    details={
                        "action": action,
                        "missing_param": required_param,
                        "provided_params": list(params.keys())
                    }
                )
    
    return True


def validate_snippet_content(snippet: str, max_length: int = 10000) -> bool:
    """
    Validate code snippet content.
    
    Args:
        snippet: Code snippet string
        max_length: Maximum allowed length
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If snippet is invalid
    """
    if not isinstance(snippet, str):
        raise ValidationError(
            "Snippet must be a string",
            details={"type": type(snippet).__name__}
        )
    
    if len(snippet) > max_length:
        raise ValidationError(
            f"Snippet too long (max {max_length} characters)",
            details={"length": len(snippet)}
        )
    
    # Check for null bytes
    if '\x00' in snippet:
        raise ValidationError("Snippet contains null bytes")
    
    return True
