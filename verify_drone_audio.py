
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(r"c:\Users\Betül Büyük\Downloads\megasentito\v8\SENTIENT_OS"))

def test_drone_audio_import():
    print("Testing drone_audio import...")
    try:
        from hardware import drone_audio
        print("Successfully imported drone_audio")
        
        # Check if QTimer is available in the module namespace
        if hasattr(drone_audio, 'QTimer'):
             print("PASS: QTimer is present in drone_audio module")
        else:
             print("FAIL: QTimer not found in drone_audio module")
             sys.exit(1)
             
    except Exception as e:
        print(f"FAIL: Import failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_drone_audio_import()
