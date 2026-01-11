import os
import sys
import time
import json
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QCoreApplication

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.function_dispatcher import FunctionDispatcher
from core.logger import log_info, log_error

class DiagnosticSuite:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.dispatcher = FunctionDispatcher()
        self.results = []
        self.log_file = os.path.join("logs", "diagnostic_results.json")
        
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def run(self):
        print("="*50)
        print(" SENTIENT_OS - Diagnostic Test Suite ")
        print("="*50)
        print("Bu araç tüm efektleri tek tek test etmenizi sağlar.")
        
        test_actions = [
            ("FAKE_NOTIFICATION", {"title": "TEST", "message": "Bu bir test bildirimidir."}),
            ("MOUSE_SHAKE", {"duration": 1.0}),
            ("OVERLAY_TEXT", {"text": "DIAGNOSTIC TEST", "duration": 2000}),
            ("FLASH_COLOR", {"color": "#FF0000", "opacity": 0.5, "duration": 500}),
            ("GDI_FLASH", {}),
            ("GDI_STATIC", {"duration": 1000}),
            ("SCREEN_INVERT", {"duration": 500}),
            ("FAKE_BSOD", {}),
            ("FAKE_FILE_DELETE", {}),
            ("TIME_DISTORTION", {}),
            ("NOTEPAD_HIJACK", {"text": "Diagnostic Test is running...", "delay": 0.05}),
            ("CORRUPT_WINDOWS", {}),
            ("RESTORE_SYSTEM", {}),
        ]
        
        # Start a thread to handle user input while Qt event loop runs
        threading.Thread(target=self._test_loop, args=(test_actions,), daemon=True).start()
        
        # Start Qt event loop
        return self.app.exec()

    def _test_loop(self, actions):
        time.sleep(1) # Wait for init
        
        for action, params in actions:
            print(f"\n[TESTING] Action: {action}")
            print(f"Params: {params}")
            
            # Dispatch action
            self.dispatcher.dispatch({"action": action, "params": params, "speech": ""})
            
            # Give it a moment to show up
            time.sleep(0.5)
            
            # Ask for feedback
            success = input(f">> Efekt düzgün mü? (y/n/skip): ").lower()
            
            if success == 'y':
                self.results.append({"action": action, "status": "SUCCESS"})
            elif success == 'n':
                reason = input(">> Hata nedeni nedir? (örn: görünmedi, ses yok): ")
                self.results.append({"action": action, "status": "FAILED", "reason": reason})
                log_error(f"Diagnostic Failure for {action}: {reason}", "DIAGNOSTIC")
            else:
                self.results.append({"action": action, "status": "SKIPPED"})

            # Cleanup some effects if needed
            if action in ["FAKE_BSOD", "NOTEPAD_HIJACK", "CORRUPT_WINDOWS"]:
                 time.sleep(1)
            
        self._save_results()
        print("\n" + "="*50)
        print(" Testler Tamamlandı! ")
        print(f" Sonuçlar kaydedildi: {self.log_file}")
        print("="*50)
        
        # Exit application
        QCoreApplication.quit()

    def _save_results(self):
        data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": self.results
        }
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    suite = DiagnosticSuite()
    sys.exit(suite.run())
