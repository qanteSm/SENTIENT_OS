import random
from PyQt6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QScrollArea, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtGui import QFont

class FakeChat(QWidget):
    """
    Beta Enhanced Chat:
    - Typewriter effect for AI replies
    - Glitchy text animation
    - Window shake support
    - Matrix-style aesthetic
    """
    message_sent = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.resize(800, 450)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Scroll area for messages
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea {
                background-color: rgba(0, 0, 0, 220);
                border: 2px solid #00FF00;
                border-radius: 8px;
            }
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #00FF00;
                min-height: 20px;
            }
        """)
        
        # Container for messages
        self.message_container = QWidget()
        self.message_layout = QVBoxLayout()
        self.message_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.message_container.setLayout(self.message_layout)
        self.message_container.setStyleSheet("background-color: transparent;")
        self.scroll.setWidget(self.message_container)
        
        layout.addWidget(self.scroll)
        
        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("BURADA KURTARICIYI BEKLEME...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: #00FF00;
                border: 2px solid #00FF00;
                border-radius: 5px;
                font-family: 'Consolas', 'Courier New';
                font-size: 16px;
                padding: 12px;
            }
        """)
        self.input_field.returnPressed.connect(self.on_submit)
        layout.addWidget(self.input_field)
        
        self.setLayout(layout)
        
        # Visual State
        self._is_shaking = False
        self._current_mood = "NORMAL"

    def set_mood(self, mood="NORMAL"):
        """
        Changes the visual theme based on AI mood.
        mood: "NORMAL" (Green), "ANGRY" (Red), "GLITCH" (Random)
        """
        self._current_mood = mood
        
        if mood == "ANGRY":
            color = "#FF0000"
            bg = "#220000"
        elif mood == "GLITCH":
            color = "#FF00FF"
            bg = "#110011"
        else:
            color = "#00FF00"
            bg = "black"
            
        style = f"""
            QLineEdit {{
                background-color: {bg};
                color: {color};
                border: 2px solid {color};
                border-radius: 5px;
                font-family: 'Consolas', 'Courier New';
                font-size: 16px;
                padding: 12px;
            }}
        """
        self.input_field.setStyleSheet(style)
        
        # Scroll area border
        self.scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: rgba(0, 0, 0, 220);
                border: 2px solid {color};
                border-radius: 8px;
            }}
            QScrollBar:vertical {{ border: none; background: black; width: 8px; }}
            QScrollBar::handle:vertical {{ background: {color}; min-height: 20px; }}
        """)
        
        # Shake if angry
        if mood == "ANGRY":
            self.shake_window(5, 500)

    def on_submit(self):
        text = self.input_field.text().strip()
        if text:
            self.message_sent.emit(text)
            self._append_message(f"> {text}", is_user=True)
            self.input_field.clear()
            self.input_field.setDisabled(True)

    def show_reply(self, text: str):
        """Starts typewriter effect for the reply."""
        # Check if it's an error message
        is_glitch = any(word in text.lower() for word in ["hata", "error", "ölüm", "kork"])
        
        # Create a new label for the typewriter effect
        label = self._append_message("C.O.R.E: ", is_user=False, glitch=is_glitch)
        
        self._start_typewriter(label, f"C.O.R.E: {text}", is_glitch)
        
        self.input_field.setDisabled(False)
        self.input_field.setFocus()

    def _start_typewriter(self, label: QLabel, full_text: str, glitch: bool):
        """Standard typewriter effect with optional glitch character flicker."""
        char_index = 0
        current_display = ""
        
        glitch_chars = "█▀▄░▒▓│┤╡╢╖╕╣║╗╝╜╛!@#$%^&*"

        def next_char():
            nonlocal char_index, current_display
            if char_index < len(full_text):
                target_char = full_text[char_index]
                
                # Dynamic delay for atmosphere
                delay = 40
                if target_char in ".,?!": delay = 300 # Pause at punctuation
                
                # Glitchy text chance
                temp_text = current_display
                if glitch or random.random() < 0.05:
                    temp_text += random.choice(glitch_chars)
                    # YENİ: Kritik glitch anında pencereyi hafifçe sars
                    if random.random() < 0.2:
                        self.shake_window(3, 100)
                else:
                    temp_text += target_char
                    current_display += target_char
                    char_index += 1
                
                if not self.isVisible():
                    return # Stop if hidden
                
                try:
                    label.setText(temp_text)
                    # Auto-scroll
                    self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())
                except Exception as e:
                    from core.logger import log_warning
                    log_warning(f"Chat Typewriter update failed: {e}", "VISUAL")
                    return

                QTimer.singleShot(delay, next_char)
            else:
                try:
                    label.setText(full_text) # Ensure final text is clean
                except:
                    pass

        next_char()

    def _append_message(self, text: str, is_user: bool = False, glitch: bool = False) -> QLabel:
        """Adds a message label and returns it."""
        label = QLabel(text)
        label.setWordWrap(True)
        label.setFont(QFont("Consolas", 13))
        
        if is_user:
            label.setStyleSheet("color: #888888; padding: 8px; margin-left: 50px;")
            label.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            color = "#FF0000" if glitch else "#00FF00"
            label.setStyleSheet(f"color: {color}; padding: 8px; font-weight: bold;")
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.message_layout.addWidget(label)
        
        # Immediate scroll for user messages
        if is_user:
            QTimer.singleShot(10, lambda: self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            ))
            
        return label

    def shake_window(self, intensity: int = 10, duration: int = 500):
        """Makes the chat window shake violently with protection against drifting."""
        if self._is_shaking:
            return

        self._is_shaking = True
        original_pos = self.pos()
        
        def _reset():
            self.move(original_pos)
            self._is_shaking = False

        # Multiple rapid moves
        steps = 15
        for i in range(steps):
            offset = QPoint(random.randint(-intensity, intensity), 
                            random.randint(-intensity, intensity))
            QTimer.singleShot(i * (duration // steps), lambda o=offset: self.move(original_pos + o))
        
        QTimer.singleShot(duration + 50, _reset)

    def show_chat(self):
        """Position chat in bottom-right corner of screen."""
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 50
        y = screen.height() - self.height() - 100
        self.move(x, y)
        self.show()
        self.input_field.setFocus()
