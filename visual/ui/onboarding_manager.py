"""
Onboarding Manager - Orchestrates the 3-step onboarding flow.

Controls the sequence: Welcome -> Calibration -> Safety/Consent
"""

from PyQt6.QtCore import QObject, pyqtSignal
from visual.ui.welcome_screen import WelcomeScreen
from visual.ui.calibration_screen import CalibrationScreen
from visual.ui.consent_screen import ConsentScreen
from core.logger import log_info, log_debug


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
        log_info("Starting onboarding flow...", "ONBOARDING")
        self._show_welcome()
    
    def _show_welcome(self):
        """Step 1: Welcome Screen"""
        self.welcome_screen = WelcomeScreen()
        self.welcome_screen.continue_clicked.connect(self._show_calibration)
        self.welcome_screen.show_welcome()
    
    def _show_calibration(self):
        """Step 2: Calibration Screen"""
        log_info("Proceeding to calibration...", "ONBOARDING")
        self.calibration_screen = CalibrationScreen()
        self.calibration_screen.calibration_complete.connect(self._on_calibration_complete)
        self.calibration_screen.show()
    
    def _on_calibration_complete(self, intensity: str):
        """Handle calibration completion"""
        self.selected_intensity = intensity
        log_info(f"Calibration complete: {intensity}", "ONBOARDING")
        self._show_consent()
    
    def _show_consent(self):
        """Step 3: Enhanced Consent Screen"""
        log_info("Proceeding to consent...", "ONBOARDING")
        self.consent_screen = ConsentScreen()
        self.consent_screen.consent_granted.connect(self._on_consent_granted)
        self.consent_screen.show_consent()
    
    def _on_consent_granted(self):
        """Handle consent granted - onboarding complete"""
        log_info(f"Onboarding complete! Intensity: {self.selected_intensity}", "ONBOARDING")
        self.onboarding_complete.emit()
