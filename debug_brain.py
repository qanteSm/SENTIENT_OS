# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import sys
import os
import threading
import time
import asyncio
from unittest.mock import MagicMock, patch

# Add core modules to path
sys.path.insert(0, os.getcwd())

from core.gemini_brain import GeminiBrain
from sdk.sentientos.models import InferenceResponse

class MockSentientClient:
    def __init__(self, *args, **kwargs):
        print(f"MockSentientClient initialized with {args} {kwargs}")
        self.call_count = 0
        self.last_request_id = None

    async def __aenter__(self):
        print("MockSentientClient entering")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("MockSentientClient exiting")
        pass

    async def infer(self, message, context, request_id=None):
        print(f"MockSentientClient.infer called with REQ-ID: {request_id}")
        return InferenceResponse(text="Hello from server", actions=[{"type": "GLITCH", "payload": {}}], cache="miss")

def debug_test():
    with patch('core.gemini_brain.ConfigManager') as mock_config_class:
        config_inst = mock_config_class.return_value
        config_inst.get.side_effect = lambda key, default=None: {
            'server.enabled': True,
            'server.edge_url': 'http://localhost:8000',
            'server.jwt_token': 'test_token',
            'server.device_id': 'test_device',
            'api.gemini_key': 'test_key'
        }.get(key, default)
        
        with patch('core.gemini_brain.HAS_SDK', True), \
             patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel'):
            
            brain = GeminiBrain()
            
            with patch('core.gemini_brain.SentientClient', side_effect=MockSentientClient):
                print(f"Patched SentientClient object in module: {sys.modules['core.gemini_brain'].SentientClient}")
                print("Calling generate_response...")
                response = brain.generate_response("Hi")
                print(f"FINAL RESPONSE: {response}")

if __name__ == "__main__":
    debug_test()
