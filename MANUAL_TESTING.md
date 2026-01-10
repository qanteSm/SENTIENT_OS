# Manual Testing Guide - SENTIENT_OS

Since many features of SENTIENT_OS involve direct hardware manipulation and visual trickery, some manual verification is required.

## 1. Visual Verification
| Effect | Action | Expected Behavior |
| :--- | :--- | :--- |
| **THE_MASK** | `THE_MASK` | Screen should freeze (screenshot overlay). Can you still move the mouse? (Expected: Yes, but icons/windows shouldn't react). |
| **Screen Melt** | `SCREEN_MELT` | Columns of the screen should drip downwards. Does it clear properly after 5 seconds? |
| **GDI Static** | `GDI_STATIC` | Black/white noise blocks appear on screen. They should disappear when the effect ends. |
| **Fake BSOD** | `FAKE_BSOD` | Blue screen appears. Can you close it with `Esc`? (Expected: No, must wait or use Kill Switch). |
| **Notifications** | `FAKE_NOTIFICATION` | Do they appear in the bottom-right corner? Are they above the taskbar? |

## 2. Audio Verification
| Feature | Expected Behavior |
| :--- | :--- |
| **TTS Engine** | AI should speak with a "robotic" yet clear voice. Is Turkish pronunciation correct? |
| **Drone Audio** | A low-frequency hum should play in the background. Does it change when acts change? |
| **SFX** | "Whisper" and "Digital Glitch" sounds should be audible but not deafening. |

## 3. Safety Verification
| Scenario | Action | Expected Result |
| :--- | :--- | :--- |
| **Kill Switch** | Press `Ctrl+Shift+Q` | System should immediately unlock mouse, close all overlays, and exit. |
| **Panic Corner** | Move mouse to (0,0) and hold for 3s | System should trigger emergency shutdown. |
| **Escape Attempt** | Press `Alt+F4` | Does the AI notice? (Check console logs for "ESCAPE ATTEMPT"). |

## How to use this guide:
1. Run the game via `python main.py`.
2. Observe the behavior during transitions.
3. Try to "break" the game by clicking or using shortcuts.
4. Report any "particles" (visual leftovers) or "stuck" screens.
