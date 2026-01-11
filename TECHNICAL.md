# TECHNICAL.md - SENTIENT_OS Architecture Guide

**For Developers**: This document provides a technical deep-dive into SENTIENT_OS architecture, design patterns, and implementation details.

---

## 📐 Architecture Overview

### System Layers

```
┌─────────────────────────────────────────┐
│         User Interface Layer            │
│  (Consent, Onboarding, Overlays, GDI)  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Application Layer               │
│   (Kernel, Dispatcher, Brain, Story)   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Service Layer                   │
│ (Sensors, Memory, State, Checkpoints)  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Hardware Layer                  │
│  (Mouse, Keyboard, Audio, GDI, Screen) │
└─────────────────────────────────────────┘
```

---

## 🏗️ Core Components

### 1. Sentient Kernel (`core/kernel.py`)

**Role:** Central orchestrator and lifecycle manager

**Responsibilities:**
- System initialization and bootstrap
- Component dependency management
- Lifecycle hooks (boot, shutdown, recovery)
- Event bus coordination
- Resource cleanup

**Design Pattern:** Singleton + Facade

```python
class SentientKernel:
    def boot(self):           # Initialize all systems
    def _complete_boot(self):  # Post-consent initialization
    def stop(self):            # Graceful shutdown
    def recovery_boot(self):   # Crash recovery path
```

**Key Features:**
- **Ordered Initialization**: Dependencies resolved before dependent  systems
- **Graceful Degradation**: Continues if non-critical components fail
- **Crash Recovery**: `sys.excepthook` override for horror-themed error handling

---

### 2. Function Dispatcher (`core/function_dispatcher.py`)

**Role:** Command pattern implementation for action execution

**Responsibilities:**
- Translate AI JSON commands to Python functions
- Route actions to appropriate hardware/visual modules
- Parameter validation and error handling
- Action logging and telemetry

**Design Pattern:** Command Pattern + Strategy

```python
def dispatch(self, command: dict):
    action = command.get("action")
    params = command.get("params", {})
    speech = command.get("speech", "")
    
    # Route to appropriate handler
    if action == "SCREEN_TEAR":
        ScreenTear.tear_screen(intensity, duration)
```

**Supported Action Categories:**
- **Visual**: Overlays, GDI effects, fake UI, masks
- **Hardware**: Mouse, keyboard, audio, brightness
- **System**: Wallpaper, clipboard, notifications
- **Horror**: Glitches, melts, tears, whispers

---

### 3. Gemini Brain (`core/gemini_brain.py`)

**Role:** AI reasoning and dialogue engine

**Responsibilities:**
- Google Gemini API integration
- Dynamic prompt construction with context
- Response caching (SHA256-based, 5-min TTL)
- Offline mode with fallback responses
- Privacy filtering (streamer mode)

**Design Pattern:** Facade + Strategy + Cache

```python
def generate_response(self, user_input: str, context: dict) -> dict:
    # 1. Check cache
    cache_key = self._get_cache_key(user_input, context)
    if cached := self._get_cached_response(cache_key):
        return cached
    
    # 2. Check offline mode
    if self._offline_mode:
        return self._offline_response(user_input, context)
    
    # 3. Call Gemini API
    prompt = self._build_dynamic_prompt(user_input, context)
    response = self.model.generate_content(prompt)
    
    # 4. Cache and return
    self._cache_response(cache_key, parsed_response)
    return parsed_response
```

**Context Sources:**
- Current Act number
- Anger level (0-100)
- Desktop folder names (file awareness)
- Active window titles
- Memory (previous interactions)
- Time of day

**Performance:**
- **Cache Hit Rate**: ~60% in testing
- **API Cost Reduction**: 60% lower than no-cache
- **Offline Mode**: Fallback responses when no internet

---

### 4. Story Manager (`story/story_manager.py`)

**Role:** Narrative progression controller

**Responsibilities:**
- Act loading and transitions
- Save/load game state
- Ambient horror intensity control
- Drone audio Act selection
- Checkpoint coordination

**Design Pattern:** State Machine + Mediator

```python
class StoryManager:
    def start_story(self):        # Begin Act 1
    def next_act(self):           # Transition to next Act
    def _load_act(self, act_num): # Load specific Act
    def set_ambient_horror(self):  # Connect ambient system
    def set_drone_audio(self):     # Connect audio system
```

**Act Configuration:**
```python
intensity_map = {
    1: 2,  # Act 1: Low ambient horror
    2: 4,  # Act 2: Medium
    3: 7,  # Act 3: High
    4: 9   # Act 4: Critical
}

drone_map = {
    1: "fan",        # Mechanical hum
    2: "static",     # TV noise
    3: "whisper",    # Creepy voices
    4: "infrasound"  # Deep 20Hz
}
```

---

## 🎨 Design Patterns Used

### 1. Singleton Pattern
**Used in:** `Config`, `StateManager`, `Memory`, `DroneAudio`

**Why:** Ensure single source of truth for global state

```python
class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

### 2. Observer Pattern
**Used in:** `Config` change notifications

**Why:** Decouple configuration changes from dependent systems

```python
class Config:
    def add_observer(self, callback):
        self._observers.append(callback)
    
    def _notify_observers(self, key, old_value, new_value):
        for observer in self._observers:
            observer(key, old_value, new_value)
```

---

### 3. Command Pattern
**Used in:** `FunctionDispatcher`

**Why:** Encapsulate actions as objects for logging, undo, queuing

```python
{
    "action": "SCREEN_TEAR",
    "params": {"intensity": 15},
    "speech": "Sistemin bütünlüğü bozuluyor..."
}
```

---

### 4. Strategy Pattern
**Used in:** AI response modes (online, offline, cached)

**Why:** Switch between algorithms at runtime

```python
if cached:
    return self._cached_strategy()
elif offline:
    return self._offline_strategy()
else:
    return self._online_strategy()
```

---

### 5. Facade Pattern
**Used in:** `SentientKernel`, `GeminiBrain`

**Why:** Simplify complex subsystem interactions

---

## 🧵 Thread Safety

### Thread Architecture

```
Main Thread (Qt Event Loop)
├── Kernel
├── Dispatcher
├── UI Components
└── Story Manager

Background Threads
├── PresenceSensor (monitors idle time)
├── WindowSensor (tracks active window)
└── ResourceGuard (monitors CPU/RAM)
```

### Thread-Safe Communication

**Pattern:** QMutex + QSignal/Slot

```python
class BaseSensor(QThread):
    sensor_data = pyqtSignal(dict)
    
    def safe_publish(self, data: Dict[str, Any]):
        self._mutex.lock()
        try:
            self.sensor_data.emit(data)
        finally:
            self._mutex.unlock()
```

**Why:**
- **Qt Threads**: Only main thread can update GUI
- **QMutex**: Prevent race conditions on shared data
- **QSignal**: Thread-safe event emission to main thread

---

## 💾 State Management

### Checkpoint System

**Location:** `core/checkpoint_manager.py`

**Features:**
- Auto-save every Act transition
- Manual save on demand
- Rolling window (keep last 5 checkpoints)
- Emergency save on crash

```python
class CheckpointManager:
    def save_checkpoint(self, label: str):
        checkpoint = {
            "timestamp": time.time(),
            "act": current_act,
            "anger": anger_level,
            "memory": memory_state
        }
        self._write_checkpoint(label, checkpoint)
```

**Storage:**
- Windows: `%APPDATA%/SentientOS/checkpoints/`
- Format: JSON
- Naming: `checkpoint_act2_1704855600.json`

---

### State Manager

**Location:** `core/state_manager.py`

**Purpose:** Track and restore system state

**Tracked State:**
- Original wallpaper path
- Original brightness level
- Desktop icon positions
- Active processes before launch

**Restore Logic:**
```python
def restore_all(self):
    # 1. Restore wallpaper
    # 2. Restore brightness
    # 3. Restore icon positions
    # 4. Close spawned processes
```

---

## 🔧 Configuration System

### YAML-Based Config

**File:** `config.yaml`

**Features:**
- Environment variable interpolation (`${VAR_NAME}`)
- Runtime modification
- Observer notifications on changes
- Validation

**Example:**
```yaml
api:
  gemini_key: "${GEMINI_API_KEY}"
  cache_ttl: 300

horror:
  intensity: "extreme"  # mild, medium, extreme
  chaos_level: 0  # 0-100
```

### ConfigManager

**Location:** `core/config_manager.py`

**Methods:**
```python
config = ConfigManager()
config.get('horror.intensity')  # Read value
config.set('horror.intensity', 'mild')  # Modify
config.save()  # Persist changes
```

**Backward Compatibility:**
```python
# Old code still works
Config().IS_MOCK  # Instance access
```

---

## 🎧 Audio System

### Drone Audio Layer

**Location:** `hardware/drone_audio.py`

**Features:**
- Infinite loop playback (pygame)
- Volume modulation by Act
- Smooth crossfading
- Multiple drone types

**Drone Types:**
```python
DRONES = {
    "fan": "fan_rumble.wav",        # Act 1
    "static": "tv_static.wav",       # Act 2
    "whisper": "distant_whispers.wav", # Act 3
    "infrasound": "infrasound_20hz.wav" # Act 4
}
```

**Technical Specs:**
- Format: WAV
- Sample Rate: 22050 Hz
- Channels: Mono/Stereo
- Loop: Infinite (`loops=-1`)

---

## 👁️ Visual Effects

### GDI Engine

**Location:** `visual/gdi_engine.py`

**Windows GDI Functions:**
- `BitBlt`: Screen region copying
- `StretchBlt`: Screen stretching
- `PatBlt`: Pattern fills
- `SetPixel`: Direct pixel manipulation

### Advanced Effects

**Screen Tear** (`visual/effects/screen_tear.py`):
```python
def tear_screen(intensity=10, duration=500):
    # 1. Capture screen to memory DC
    # 2. Copy slices with horizontal offset
    # 3. Auto-restore after duration
```

**Pixel Melt** (`visual/effects/pixel_melt.py`):
```python
def melt_region(x, y, width, height):
    # 1. Capture region
    # 2. Shift pixels downward (dripping effect)
    # 3. Apply per-column random drip amount
```

**Safety:**
- Non-destructive (temporary only)
- Auto-restore via `InvalidateRect`
- Respects `SAFE_HARDWARE` config

---

## 📊 Performance Optimization

### AI Response Caching

**Strategy:** SHA256-based cache keys with 5-min TTL

**Cache Key Construction:**
```python
def _get_cache_key(self, user_input: str, context: dict) -> str:
    cache_context = {
        'persona': self.current_persona,
        'anger': context.get('anger_level', 0) // 10  # Bucket
    }
    combined = f"{user_input}:{json.dumps(cache_context)}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]
```

**Performance:**
- **Latency:** 50ms (cached) vs 2-5s (API)
- **Cost:** $0 (cached) vs $0.0001/request (API)
- **Hit Rate:** ~60% in typical gameplay

---

### Dynamic Event Scheduling

**Location:** `story/dynamic_scheduler.py`

**Algorithm:**
```python
def _calculate_adaptive_delay(self, min_delay, max_delay):
    idle_factor = min(user_idle_time / 30.0, 1.0)
    compression = 1.0 - (idle_factor * 0.6)  # 60% max compression
    
    delay_range = max_delay - min_delay
    compressed_range = delay_range * compression
    
    actual_delay = min_delay + random.uniform(0, compressed_range)
    return int(actual_delay)
```

**Effect:**
- **Idle User (30s+):** Events fire every 8-15s
- **Active User:** Events fire every 30-60s
- **Prevents:** "Game frozen?" perception

---

## 🛡️ Safety Systems

### Multi-Layer Protection

#### 1. Kill Switch
```python
# Global keyboard hook
if key == 'q' and ctrl_pressed and shift_pressed:
    kernel.emergency_shutdown()
```

#### 2. Resource Guard
```python
if psutil.cpu_percent() > 85 or psutil.virtual_memory().percent > 85:
    kernel.safe_shutdown("Resource threshold exceeded")
```

#### 3. Panic Sensor
```python
# ESC key spam detection
if esc_presses_last_2s > 5:
    kernel.shutdown("Panic detected")
```

#### 4. Crash Handler
```python
sys.excepthook = CrashHandler._handle_exception

def _handle_exception(exc_type, exc_value, exc_traceback):
    # 1. Log error
    # 2. Save emergency checkpoint
    # 3. Show fake crash screen (horror)
    # 4. Auto-recover after 3s
```

---

## 📁 Project Structure

```
sentient_os/
├── main.py                 # Entry point
├── config.yaml             # Runtime configuration
├── launcher.py             # Pre-flight checks
│
├── core/                   # Core systems
│   ├── kernel.py           # Central orchestrator
│   ├── function_dispatcher.py  # Command router
│   ├── gemini_brain.py     # AI engine
│   ├── memory.py           # Conversation memory
│   ├── state_manager.py    # System state tracking
│   ├── checkpoint_manager.py   # Save system
│   ├── config_manager.py   # YAML config
│   ├── crash_handler.py    # Exception handling
│   ├── file_awareness.py   # Desktop scanning
│   └── sensors/            # Background threads
│       ├── base_sensor.py  # Thread-safe base
│       ├── presence_sensor.py  # Idle detection
│       └── window_sensor.py    # Active window
│
├── story/                  # Narrative systems
│   ├── story_manager.py    # Act controller
│   ├── dynamic_scheduler.py    # Adaptive timing
│   ├── silence_breaker.py  # Idle event trigger
│   └── acts/               # Act implementations
│       ├── act_1_infection.py
│       ├── act_2_awakening.py
│       ├── act_3_torment.py
│       └── act_4_exorcism.py
│
├── visual/                 # Visual systems
│   ├── overlay_manager.py  # Text/flash overlays
│   ├── fake_ui.py          # Fake system UI
│   ├── desktop_mask.py     # Screen freeze
│   ├── gdi_engine.py       # Low-level GDI
│   ├── ambient_horror.py   # Background effects
│   ├── ui/                 # User interface
│   │   ├── welcome_screen.py
│   │   ├── calibration_screen.py
│   │   └── onboarding_manager.py
│   └── effects/            # Advanced effects
│       ├── screen_tear.py
│       └── pixel_melt.py
│
├── hardware/               # Hardware control
│   ├── mouse_ops.py        # Mouse manipulation
│   ├── keyboard_ops.py     # Keyboard control
│   ├── audio_out.py        # TTS + sound
│   ├── brightness_ops.py   # Screen brightness
│   ├── drone_audio.py      # Atmospheric audio
│   └── wallpaper_ops.py    # Desktop wallpaper
│
└── assets/                 # Resources
    └── audio/drones/       # Ambient audio files
```

---

## 🔌 API Integration

### Google Gemini API

**Model:** `gemini-2.5-flash`

**Configuration:**
```python
generation_config = {
    "temperature": 1.0,  # Creativity
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
}
```

**Safety Settings:** Disabled (for horror content)

**Response Format:** JSON
```json
{
    "action": "OVERLAY_TEXT",
    "params": {
        "text": "Senle konuşmak istiyorum...",
        "duration": 3000
    },
    "speech": "Merhaba kullanıcı..."
}
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/unit/
```

### Integration Tests
```bash
pytest tests/integration/
```

### Manual Testing
```python
# Crash recovery test
from core.crash_handler import CrashHandler
CrashHandler.test_crash()

# GDI effects test
from visual.effects.screen_tear import ScreenTear
ScreenTear.trigger_random()
```

---

## 📈 Metrics & Telemetry

### Tracked Metrics
- API call count
- Cache hit rate
- Average response time
- Act completion time
- User idle time
- Resource usage (CPU/RAM)

### Logging
```python
from core.logger import log_info, log_error

log_info("User accepted consent", "KERNEL")
log_error(f"API call failed: {e}", "BRAIN")
```

**Log Location:** `logs/sentient_os.log`

---

---

## 🛡️ Robustness & Anti-Fragility

SENTIENT_OS isn't just stable; it's designed to withstand catastrophic failures through advanced testing methodologies.

### 🐒 Chaos Engineering
We employ **Chaos Monkey** testing to simulate worst-case scenarios:
- **Catastrophic Shutdown**: Simulated "Alt+F4" or `sys.exit(1)` exactly during an Act transition or memory write.
- **State Preservation**: Verified that JSON save files remain valid (atomic writes) even if the process is killed mid-operation.
- **Race Condition Hunting**: 100+ concurrent operations on shared resources to ensure lock integrity.

### 🏎️ Stress Verification
The system has been benchmarked for extreme performance:
- **Dispatcher Throughput**: ~410 actions per second (4x the required peak load).
- **Resource Guard**: Automated detection of "Staircase Effect" memory leaks.
- **Zero GDI Leaks**: Specialized tracking for Windows GDI handles, ensuring 100% garbage collection of screen resources.

### 🎖️ Performance Standards
| Metric | Threshold | Performance |
|--------|-----------|-------------|
| **Save Latency** | < 100ms | ~12ms |
| **GDI Handle Peak** | 10,000 (Win Limit) | < 150 |
| **State Integrity** | 100% | 100% |
| **Crash Recovery** | < 3.0s | ~2.1s |

---

## 🚦 Development Guidelines

### Code Style
- **PEP 8** compliance
- **Type hints** for public APIs
- **Docstrings** for all classes/methods
- **Comments** for complex logic

### Adding New Actions

1. **Define action in Dispatcher:**
```python
elif action == "NEW_ACTION":
    params = command.get("params", {})
    self.hardware.new_action(params)
```

2. **Implement handler:**
```python
# hardware/new_module.py
def new_action(params):
    # Implementation
    pass
```

3. **Update AI context:**
```python
# Add to gemini_brain.py prompt
"Available actions: ..., NEW_ACTION"
```

---

## 🔐 Security Considerations

### Privacy
- **No data collection**: All data stays local
- **Privacy filter**: Scrubs usernames, paths before AI
- **API key**: Stored as environment variable only

### Safety
- **SAFE_HARDWARE mode**: Disables risky effects
- **Validation**: All AI responses validated before execution
- **Emergency exit**: Multiple fail-safes

### Sandboxing
- **Read-only file access**: Desktop scanning doesn't modify files
- **Reversible changes**: All system modifications auto-revert
- **Process protection**: Won't terminate critical processes

---

## 📚 Further Reading

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Windows GDI Reference](https://docs.microsoft.com/en-us/windows/win32/gdi/windows-gdi)

---

**Built with engineering excellence for maximum immersion** 🧠⚡
