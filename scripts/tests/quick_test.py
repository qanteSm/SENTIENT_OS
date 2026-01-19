# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

# Quick Test Script for Developer Mode
# Run this to quickly test if the game launches without admin prompts

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from config import Config

# Enable dev mode temporarily
config = Config()
original_dev_mode = config.get("DEV_MODE", False)

print("=" * 60)
print(" QUICK TEST - Temporary DEV_MODE Activation")
print("=" * 60)
print(f"Current DEV_MODE: {original_dev_mode}")
print("\nTo permanently enable DEV_MODE:")
print("  1. Open config.yaml")
print("  2. Set system.DEV_MODE: true")
print("\nThen just run: python launcher.py")
print("=" * 60)
