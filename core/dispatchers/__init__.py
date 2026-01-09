"""
Specialized dispatchers for SENTIENT_OS.

This package contains action dispatchers organized by category:
- visual: Screen effects, overlays, GDI operations
- hardware: Mouse, keyboard, audio, camera control
- horror: Horror-specific effects and scares
- system: System operations, config, cleanup
"""

from core.dispatchers.base_dispatcher import BaseDispatcher

__all__ = ['BaseDispatcher']
