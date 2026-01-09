# SENTIENT_OS API Reference

> Auto-generated API documentation for SENTIENT_OS v4.0

## Core Modules

### config_manager.py

#### ConfigManager

Configuration management with YAML file support.

**Methods:**
- `__init__(config_path="config.yaml")` - Initialize config manager
- `load_config()` - Load configuration from YAML file
- `get(key_path, default=None)` - Get config value using dot notation (e.g., "system.language")
- `set(key_path, value)` - Set config value
- `save_config(output_path=None)` - Save configuration to file
- `reload()` - Reload configuration from file

**Example:**
```python
from core.config_manager import get_config_manager

config = get_config_manager()
language = config.get('system.language', 'en')
config.set('safety.chaos_level', 5)
```

---

### error_tracker.py

#### ErrorTracker

Centralized error tracking and recovery.

**Severity Levels:**
- `SEVERITY_DEBUG` - Detailed diagnostic information
- `SEVERITY_INFO` - General informational messages
- `SEVERITY_WARNING` - Warning about potential issues  
- `SEVERITY_ERROR` - Error events
- `SEVERITY_CRITICAL` - Serious errors requiring immediate attention

**Methods:**
- `track_error(error, context=None, severity="ERROR", component="UNKNOWN")` - Track an exception
- `track_message(message, severity="INFO", component="SYSTEM", context=None)` - Track a message
- `get_session_summary()` - Get error statistics for current session
- `get_errors_by_component(component)` - Get errors for specific component
- `clear_session()` - Clear session error history
- `export_session_log(output_path)` - Export errors to file

**Example:**
```python
from core.error_tracker import track_error, track_message

try:
    risky_operation()
except Exception as e:
    track_error(e, context={"user_id": 123}, severity="ERROR", component="API")

track_message("System initialized", severity="INFO", component="KERNEL")
```

---

For full documentation, see individual module docstrings.

**Last Updated:** January 9, 2026  
**Version:** 4.0
