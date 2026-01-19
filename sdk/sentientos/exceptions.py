# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

class SentientError(Exception):
    """Base exception for SENTIENT_OS SDK"""
    pass

class AuthenticationError(SentientError):
    """Raised when authentication fails"""
    pass

class RateLimitError(SentientError):
    """Raised when the rate limit is exceeded"""
    pass

class SecurityBlockError(SentientError):
    """Raised when the client is blocked by security protocols"""
    pass

class CommunicationError(SentientError):
    """Raised when there is a connection or server error"""
    pass
