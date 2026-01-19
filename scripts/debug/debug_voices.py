# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import pyttsx3

try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"--- AVAILABLE VOICES ({len(voices)}) ---")
    for i, voice in enumerate(voices):
        print(f"[{i}] ID: {voice.id}")
        print(f"    Name: {voice.name}")
        print(f"    Languages: {voice.languages}")
        print(f"    Gender: {voice.gender}")
        print(f"    Age: {voice.age}")
        print("-" * 20)
except Exception as e:
    print(f"Error listing voices: {e}")
