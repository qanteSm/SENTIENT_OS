"""
Onboarding Manager - Orchestrates the 3-step onboarding flow.

Controls the sequence: Welcome -> Calibration -> Safety/Consent
"""

from PyQt6.QtCore import QObject, pyqtSignal
from visual.ui.welcome_screen import WelcomeScreen
from visual.ui.calibration_screen import CalibrationScreen
from visual.ui.consent_screen import ConsentScreen


class OnboardingManager(QObject):
    """
    Manages the complete onboarding experience.
    
    Flow:
    1. Welcome Screen (atmospheric intro)
    2. Calibration Screen (intensity selection)
    3. Safety/Consent Screen (legal + safety)
    """
    
    onboarding_complete = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.welcome_screen = None
        self.calibration_screen = None
        self.consent_screen = None
        
        self.selected_intensity = "extreme"
    
    def start_onboarding(self):
        """Begin the onboarding sequence"""
        print("[ONBOARDING] Starting onboarding flow...")
        self._show_welcome()
    
    def _show_welcome(self):
        """Step 1: Welcome Screen"""
        self.welcome_screen = WelcomeScreen()
        self.welcome_screen.continue_clicked.connect(self._show_calibration)
        self.welcome_screen.show_welcome()
    
    def _show_calibration(self):
        """Step 2: Calibration Screen"""
        print("[ONBOARDING] Proceeding to calibration...")
        self.calibration_screen = CalibrationScreen()
        self.calibration_screen.calibration_complete.connect(self._on_calibration_complete)
        self.calibration_screen.show()
    
    def _on_calibration_complete(self, intensity: str):
        """Handle calibration completion"""
        self.selected_intensity = intensity
        print(f"[ONBOARDING] Calibration complete: {intensity}")
        self._show_consent()
    
    def _show_consent(self):
        """Step 3: Enhanced Consent Screen"""
        print("[ONBOARDING] Proceeding to consent...")
        self.consent_screen = ConsentScreen()
        self.consent_screen.consent_granted.connect(self._on_consent_granted)
        self.consent_screen.show_consent()
    
    def _on_consent_granted(self):
        """Handle consent granted - onboarding complete"""
        print(f"[ONBOARDING] Onboarding complete! Intensity: {self.selected_intensity}")
        self.onboarding_complete.emit()
