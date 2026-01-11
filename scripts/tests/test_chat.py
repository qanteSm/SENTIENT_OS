"""
Quick Chat Test - Verifies chat works without full game loop
"""
import sys
from PyQt6.QtWidgets import QApplication
from core.gemini_brain import GeminiBrain
from visual.fake_chat import FakeChat

def test_chat():
    app = QApplication(sys.argv)
    
    brain = GeminiBrain()
    print(f"Brain mode: {'MOCK' if brain.mock_mode else 'GEMINI'}")
    
    chat = FakeChat()
    
    def handle_message(text):
        print(f"[TEST] User typed: {text}")
        
        # Immediate test response
        chat.show_reply(f"Test cevap: '{text}' aldım")
        
        # Then try real AI
        def on_ai_response(resp):
            print(f"[TEST] AI responded: {resp}")
            if resp:
                chat.show_reply(resp.get("speech", "Hata"))
        
        brain.generate_async(text, on_ai_response)
    
    chat.message_sent.connect(handle_message)
    chat.show_chat()
    
    print("[TEST] Chat window shown. Type something and press Enter.")
    sys.exit(app.exec())

if __name__ == "__main__":
    test_chat()
