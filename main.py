import sys
import atexit
import signal
from core.kernel import SentientKernel
from core.logger import log_info, log_error

def main():
    """
    SENTIENT_OS Bootloader.
    The actual logic is managed by the SentientKernel.
    """
    kernel = SentientKernel()
    
    # Register global exit handlers
    atexit.register(kernel.shutdown)
    
    try:
        signal.signal(signal.SIGTERM, lambda s, f: kernel.shutdown())
        signal.signal(signal.SIGINT, lambda s, f: kernel.shutdown())
    except:
        pass # Signal handlers vary by OS

    try:
        kernel.boot()
    except Exception as e:
        log_error(f"Sistem önyükleme sırasında çöktü: {e}", "BOOT")
        kernel.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main()
