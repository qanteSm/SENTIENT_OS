# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

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
