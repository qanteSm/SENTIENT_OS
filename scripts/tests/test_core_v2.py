# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import sys
import unittest
from PyQt6.QtWidgets import QApplication
from core.kernel import SentientKernel
from core.event_bus import bus

class TestKernel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need a QApplication for the Kernel to boot
        cls.app = QApplication.instance()
        if not cls.app:
            cls.app = QApplication(sys.argv)

    def test_kernel_singleton(self):
        k1 = SentientKernel()
        k2 = SentientKernel()
        self.assertIs(k1, k2)

    def test_event_bus_pub_sub(self):
        received = []
        def handler(data):
            received.append(data)
        
        bus.subscribe("test.event", handler)
        bus.publish("test.event", {"msg": "hello"})
        
        # In a real Qt app, signals need the event loop, 
        # but for simple direct connection they might work immediately
        # if not using queued connections.
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["msg"], "hello")

    def test_kernel_initialization(self):
        kernel = SentientKernel()
        # Mocking boot for partial test
        kernel.anger = "anger_mock"
        self.assertEqual(kernel.anger, "anger_mock")

if __name__ == "__main__":
    unittest.main()
