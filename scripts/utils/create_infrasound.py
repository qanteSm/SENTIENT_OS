# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================



import wave
import math
import struct
import os

def create_infrasound():
    # Settings
    filename = "assets/audio/drones/infrasound_20hz.wav"
    frequency = 25  # Hz
    duration = 20   # seconds
    sample_rate = 22050
    amplitude = 0.3
    
    # Create directory
    os.makedirs("assets/audio/drones", exist_ok=True)
    
    # Calculate samples
    num_samples = int(sample_rate * duration)
    
    # Open WAV file
    with wave.open(filename, 'w') as wav_file:
        # Configure: mono, 2 bytes per sample, sample rate
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        # Generate and write samples
        for i in range(num_samples):
            # Calculate sine wave
            t = i / sample_rate
            sample = amplitude * math.sin(2 * math.pi * frequency * t)
            
            # Add slight variation
            variation = 0.05 * math.sin(2 * math.pi * 0.1 * t)
            sample = sample * (1 + variation)
            
            # Convert to 16-bit integer
            sample_int = int(sample * 32767)
            
            # Pack and write
            wav_file.writeframes(struct.pack('<h', sample_int))
    
    # Get file size
    size_kb = os.path.getsize(filename) / 1024
    
    print(f"✓ Created: {filename}")
    print(f"  Frequency: {frequency} Hz")
    print(f"  Duration: {duration} seconds")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"\n✓ Infrasound ready!")

if __name__ == "__main__":
    create_infrasound()
