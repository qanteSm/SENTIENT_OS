# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

import win32com.client

try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    print(f"--- SAPI5 VOICES ({voices.Count}) ---")
    for i in range(voices.Count):
        v = voices.Item(i)
        print(f"[{i}] {v.GetDescription()}")
    
    # Try search by name
    print("\nAttempting to find Tolga specifically...")
    try:
        # Use a filter
        tolga_voices = speaker.GetVoices("Name=Microsoft Tolga")
        if tolga_voices.Count > 0:
            print(f"Found Tolga via filter! Brand: {tolga_voices.Item(0).GetDescription()}")
        else:
            print("Tolga not found via filter.")
    except Exception as e:
        print(f"Filter error: {e}")

except Exception as e:
    print(f"SAPI error: {e}")
