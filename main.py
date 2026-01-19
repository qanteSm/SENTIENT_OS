# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import sys
import atexit
import signal
from core.kernel import SentientKernel
from core.logger import log_info, log_error
from core.crash_handler import install_crash_handler

def main():
    """
    SENTIENT_OS Bootloader.
    The actual logic is managed by the SentientKernel.
    """
    # CRITICAL: Install crash handler FIRST
    install_crash_handler()
    import faulthandler
    faulthandler.enable()
    
    kernel = SentientKernel()
    
    # Register global exit handlers
    atexit.register(kernel.shutdown)
    
    try:
        signal.signal(signal.SIGTERM, lambda s, f: kernel.shutdown())
        signal.signal(signal.SIGINT, lambda s, f: kernel.shutdown())
    except (AttributeError, ValueError, OSError) as e:
        log_info(f"Signal handlers not available on this OS: {e}", "BOOT")
        pass # Signal handlers vary by OS

    try:
        kernel.boot()
    except Exception as e:
        log_error(f"Sistem önyükleme sırasında çöktü: {e}", "BOOT")
        kernel.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main()
