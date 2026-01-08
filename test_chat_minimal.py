"""
MINIMAL Chat Test - Strips out all complexity
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from core.gemini_brain import GeminiBrain
from visual.fake_chat import FakeChat

def main():
    app = QApplication(sys.argv)
    
    brain = GeminiBrain()
    print(f"[TEST] Brain initialized. Mock mode: {brain.mock_mode}")
    
    chat = FakeChat()
    chat.show_chat()
    
    def on_user_message(text):
        print(f"\n[TEST] ===== USER TYPED: {text} =====")
        
        # Show immediate feedback
        chat.show_reply(f"Alındı: '{text}'")
        
        # Call AI after 1 second delay (to see immediate response first)
        def call_ai():
            print("[TEST] Calling AI...")
            
            def on_response(resp):
                print(f"[TEST] ===== GOT RESPONSE: {resp} =====")
                if resp and "speech" in resp:
                    chat.show_reply(f"AI: {resp['speech']}")
                else:
                    chat.show_reply(f"Hata: {resp}")
            
            brain.generate_async(text, on_response)
        
        QTimer.singleShot(1000, call_ai)
    
    chat.message_sent.connect(on_user_message)
    
    print("\n[TEST] Ready. Type something and press Enter.")
    print("[TEST] You should see TWO responses:")
    print("[TEST]   1. Immediate 'Alındı' confirmation")
    print("[TEST]   2. AI response after ~1 second\n")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
