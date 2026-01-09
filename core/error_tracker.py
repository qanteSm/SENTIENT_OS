"""
Error Tracker for SENTIENT_OS
Centralized error tracking, logging, and recovery system.
"""
import traceback
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class ErrorTracker:
    """
    Centralized error tracking and reporting system.
    Tracks errors with context, severity levels, and provides recovery mechanisms.
    """
    
    SEVERITY_DEBUG = "DEBUG"
    SEVERITY_INFO = "INFO"
    SEVERITY_WARNING = "WARNING"
    SEVERITY_ERROR = "ERROR"
    SEVERITY_CRITICAL = "CRITICAL"
    
    def __init__(self, log_dir="logs/errors"):
        """
        Initialize error tracker.
        
        Args:
            log_dir: Directory for error logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.session_errors: List[Dict[str, Any]] = []
        self.error_count = {
            self.SEVERITY_DEBUG: 0,
            self.SEVERITY_INFO: 0,
            self.SEVERITY_WARNING: 0,
            self.SEVERITY_ERROR: 0,
            self.SEVERITY_CRITICAL: 0
        }
    
    def track_error(
        self, 
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        severity: str = "ERROR",
        component: str = "UNKNOWN"
    ) -> Dict[str, Any]:
        """
        Track an error with context information.
        
        Args:
            error: The exception that occurred
            context: Additional context information
            severity: Error severity level
            component: Component where error occurred
            
        Returns:
            dict: Error data that was logged
        """
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "component": component,
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        self.session_errors.append(error_data)
        self.error_count[severity] = self.error_count.get(severity, 0) + 1
        
        # Write to file
        self._write_to_file(error_data)
        
        # Trigger recovery for critical errors
        if severity == self.SEVERITY_CRITICAL:
            self._trigger_recovery(error_data)
        
        # Print to console
        self._print_error(error_data)
        
        return error_data
    
    def track_message(
        self,
        message: str,
        severity: str = "INFO",
        component: str = "SYSTEM",
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Track a message without an exception.
        
        Args:
            message: Message to log
            severity: Message severity
            component: Component logging the message
            context: Additional context
        """
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "component": component,
            "type": "Message",
            "message": message,
            "traceback": None,
            "context": context or {}
        }
        
        self.session_errors.append(error_data)
        self.error_count[severity] = self.error_count.get(severity, 0) + 1
        self._write_to_file(error_data)
        self._print_error(error_data)
    
    def _write_to_file(self, error_data: Dict[str, Any]):
        """Write error data to daily log file."""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"errors_{today}.jsonl"
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                json.dump(error_data, f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            print(f"[ERROR_TRACKER] Failed to write log: {e}", file=sys.stderr)
    
    def _print_error(self, error_data: Dict[str, Any]):
        """Print error to console with formatting."""
        severity = error_data['severity']
        component = error_data['component']
        message = error_data['message']
        
        # Color codes for terminal
        colors = {
            self.SEVERITY_DEBUG: '\033[36m',      # Cyan
            self.SEVERITY_INFO: '\033[32m',       # Green
            self.SEVERITY_WARNING: '\033[33m',    # Yellow
            self.SEVERITY_ERROR: '\033[31m',      # Red
            self.SEVERITY_CRITICAL: '\033[35m'    # Magenta
        }
        reset = '\033[0m'
        
        color = colors.get(severity, reset)
        print(f"{color}[{severity}]{reset} [{component}] {message}", file=sys.stderr)
        
        # Print traceback for errors
        if error_data['traceback'] and severity in [self.SEVERITY_ERROR, self.SEVERITY_CRITICAL]:
            print(f"  Traceback: {error_data['traceback'][:200]}...", file=sys.stderr)
    
    def _trigger_recovery(self, error_data: Dict[str, Any]):
        """
        Trigger recovery procedures for critical errors.
        
        Args:
            error_data: Error information
        """
        print(f"[RECOVERY] Critical error detected in {error_data['component']}", file=sys.stderr)
        print(f"[RECOVERY] Attempting automatic recovery...", file=sys.stderr)
        
        # Log recovery attempt
        self.track_message(
            f"Recovery triggered for: {error_data['message']}",
            severity=self.SEVERITY_WARNING,
            component="RECOVERY",
            context={"original_error": error_data['type']}
        )
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get summary of errors in current session.
        
        Returns:
            dict: Error count by severity and recent errors
        """
        return {
            "total_errors": len(self.session_errors),
            "by_severity": self.error_count.copy(),
            "recent_errors": self.session_errors[-10:] if self.session_errors else []
        }
    
    def get_errors_by_component(self, component: str) -> List[Dict[str, Any]]:
        """
        Get all errors for a specific component.
        
        Args:
            component: Component name
            
        Returns:
            list: Errors from that component
        """
        return [e for e in self.session_errors if e['component'] == component]
    
    def clear_session(self):
        """Clear session error history."""
        self.session_errors.clear()
        for key in self.error_count:
            self.error_count[key] = 0
    
    def export_session_log(self, output_path: str):
        """
        Export session errors to file.
        
        Args:
            output_path: Path to export file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "session_summary": self.get_session_summary(),
                "all_errors": self.session_errors
            }, f, indent=2, ensure_ascii=False)


# Global error tracker instance
_error_tracker: Optional[ErrorTracker] = None


def get_error_tracker() -> ErrorTracker:
    """
    Get global error tracker instance (singleton).
    
    Returns:
        ErrorTracker: Global error tracker
    """
    global _error_tracker
    if _error_tracker is None:
        _error_tracker = ErrorTracker()
    return _error_tracker


def track_error(error: Exception, context: Optional[Dict[str, Any]] = None, 
                severity: str = "ERROR", component: str = "UNKNOWN"):
    """
    Convenience function to track an error.
    
    Args:
        error: Exception to track
        context: Additional context
        severity: Error severity
        component: Component name
    """
    return get_error_tracker().track_error(error, context, severity, component)


def track_message(message: str, severity: str = "INFO", component: str = "SYSTEM",
                 context: Optional[Dict[str, Any]] = None):
    """
    Convenience function to track a message.
    
    Args:
        message: Message to log
        severity: Message severity
        component: Component name
        context: Additional context
    """
    get_error_tracker().track_message(message, severity, component, context)
