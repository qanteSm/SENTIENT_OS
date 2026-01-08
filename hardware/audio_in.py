from config import Config
try:
    if Config.IS_MOCK:
        raise ImportError("Mock Mode")
    import sounddevice as sd
    import numpy as np
except ImportError:
    sd = None
    np = None

class AudioIn:
    """
    Handles microphone listening and noise floor calibration.
    """
    def __init__(self):
        self.threshold = 0.5 # Default arbitrary RMS
        self.calibrated = False

    def calibrate_noise_floor(self, duration=3):
        """Measures ambient noise for `duration` seconds."""
        if Config.IS_MOCK or not sd:
            print("[MOCK] CALIBRATING AUDIO NOISE FLOOR...")
            self.threshold = 50
            self.calibrated = True
            return
        
        print(f"[AUDIO_IN] Calibrating for {duration} seconds... Please stay silent.")
        try:
            fs = 44100  # Sample rate
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            
            # Calculate RMS (Root Mean Square)
            rms = np.sqrt(np.mean(recording**2))
            
            # Set threshold to 1.5x of ambient noise or minimum 0.05
            self.threshold = max(0.05, rms * 1.5)
            self.calibrated = True
            print(f"[AUDIO_IN] Calibration complete. Threshold: {self.threshold:.4f}")
        except Exception as e:
            print(f"[AUDIO_IN] Calibration Failed: {e}")

    def listen_for_scream(self, duration=1):
        """Returns True if input volume exceeds threshold significantly."""
        if Config.IS_MOCK or not sd:
            return False
        
        try:
            fs = 44100
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            
            current_rms = np.sqrt(np.mean(recording**2))
            
            # If current noise is 3x the threshold -> SCREAM
            if current_rms > (self.threshold * 3.0):
                print(f"[AUDIO_IN] SCREAM DETECTED! (Level: {current_rms:.4f})")
                return True
            return False
        except Exception as e:
            print(f"[AUDIO_IN] Listen Error: {e}")
            return False
