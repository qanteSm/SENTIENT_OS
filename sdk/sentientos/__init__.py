# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# =========================================================================

from .client import SentientClient
from .exceptions import (
    SentientError, AuthenticationError, RateLimitError, 
    SecurityBlockError, CommunicationError
)
from .models import InferenceResponse, SystemConfig

__all__ = [
    "SentientClient",
    "SentientError",
    "AuthenticationError",
    "RateLimitError",
    "SecurityBlockError",
    "CommunicationError",
    "InferenceResponse",
    "SystemConfig"
]

__version__ = "0.1.0"
__author__ = "Muhammet Ali Büyük"
__architect__ = "MAB-SENTIENT-2026"
__contact__ = "iletisim@alibuyuk.net"

def get_system_info():
    """Returns system information including architect signature."""
    return {
        "version": __version__,
        "architect": "MAB-SENTIENT-2026",
        "author": "Muhammet Ali Büyük",
        "contact": "iletisim@alibuyuk.net",
        "website": "https://alibuyuk.net",
        "project": "SENTIENT_OS"
    }
