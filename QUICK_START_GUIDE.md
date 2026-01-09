# 🚀 Quick Start Implementation Guide

> Hızlı başlangıç rehberi - En kritik iyileştirmelerden başlayın!  
> Quick start guide - Begin with the most critical improvements!

---

## 🎯 İlk 4 Hafta İçin Pratik Plan / Practical Plan for First 4 Weeks

### Hafta 1 / Week 1: Configuration System

#### Hedef / Goal
Hardcoded ayarları YAML/JSON config dosyasına taşı

#### Adımlar / Steps

1. **config.yaml oluştur**
```yaml
# config.yaml
system:
  app_name: "SENTIENT_OS"
  version: "4.0"
  language: "tr"
  
api:
  gemini_key: "${GEMINI_API_KEY}"
  model: "gemini-2.5-flash"
  
safety:
  streamer_mode: true
  safe_hardware: false
  enable_strobe: false
  chaos_level: 0
  
performance:
  max_cpu_percent: 85
  max_ram_percent: 80
```

2. **ConfigManager sınıfı ekle**
```python
# core/config_manager.py
import yaml
import os

class ConfigManager:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        # Environment variable substitution
        return self._substitute_env_vars(config)
    
    def get(self, key_path, default=None):
        """Get nested config value: 'system.language'"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            value = value.get(key, default)
            if value is None:
                return default
        return value
```

3. **config.py'yi refactor et**
```python
# config.py
from core.config_manager import ConfigManager

_config = ConfigManager()

class Config:
    # Load from config.yaml
    APP_NAME = _config.get('system.app_name', 'SENTIENT_OS')
    VERSION = _config.get('system.version', '4.0')
    LANGUAGE = _config.get('system.language', 'tr')
    # ... etc
```

#### Test / Testing
```bash
python -c "from config import Config; print(Config.APP_NAME)"
```

---

### Hafta 2 / Week 2: Error Handling

#### Hedef / Goal
Merkezi error tracking ve logging sistemi

#### Adımlar / Steps

1. **ErrorTracker sınıfı oluştur**
```python
# core/error_tracker.py
import traceback
import json
from datetime import datetime
from pathlib import Path

class ErrorTracker:
    """Centralized error tracking and reporting"""
    
    def __init__(self, log_dir="logs/errors"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.session_errors = []
    
    def track_error(self, error, context=None, severity="ERROR"):
        """Track an error with context"""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        self.session_errors.append(error_data)
        self._write_to_file(error_data)
        
        if severity == "CRITICAL":
            self._trigger_recovery(error_data)
    
    def _write_to_file(self, error_data):
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"errors_{today}.json"
        
        with open(log_file, 'a') as f:
            json.dump(error_data, f)
            f.write('\n')
```

2. **Mevcut kodda kullan**
```python
# Example usage in kernel.py
from core.error_tracker import ErrorTracker

class SentientKernel:
    def __init__(self):
        self.error_tracker = ErrorTracker()
    
    def boot(self):
        try:
            # ... existing code
        except Exception as e:
            self.error_tracker.track_error(
                e, 
                context={"phase": "boot", "component": "kernel"},
                severity="CRITICAL"
            )
            raise
```

---

### Hafta 3 / Week 3: Basic Testing

#### Hedef / Goal
Test infrastructure ve ilk unit testler

#### Adımlar / Steps

1. **pytest kur**
```bash
pip install pytest pytest-cov pytest-mock
```

2. **Test yapısı oluştur**
```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_memory.py
│   ├── test_event_bus.py
│   └── test_config_manager.py
└── integration/
    ├── __init__.py
    └── test_story_flow.py
```

3. **İlk testleri yaz**
```python
# tests/unit/test_event_bus.py
import pytest
from core.event_bus import EventBus

class TestEventBus:
    def test_subscribe_and_publish(self):
        bus = EventBus()
        received = []
        
        def handler(data):
            received.append(data)
        
        bus.subscribe("test.event", handler)
        bus.publish("test.event", {"value": 42})
        
        assert len(received) == 1
        assert received[0]["value"] == 42
    
    def test_unsubscribe(self):
        bus = EventBus()
        received = []
        
        def handler(data):
            received.append(data)
        
        bus.subscribe("test.event", handler)
        bus.unsubscribe("test.event", handler)
        bus.publish("test.event", {"value": 42})
        
        assert len(received) == 0
```

4. **GitHub Actions CI ekle**
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=core --cov-report=html
```

#### Test / Testing
```bash
pytest tests/ -v
pytest tests/ --cov=core --cov-report=html
```

---

### Hafta 4 / Week 4: Documentation

#### Hedef / Goal
Kod içi dokümantasyon ve API referansı

#### Adımlar / Steps

1. **Docstring standardı belirle**
```python
# Example: Google Style Docstrings
def think(self, prompt: str, context: dict = None) -> dict:
    """Process user input and generate AI response.
    
    Args:
        prompt: User message or system prompt
        context: Optional contextual information including:
            - files: List of desktop files
            - windows: Active window information
            - time: Current system time
    
    Returns:
        Dictionary containing:
            - response (str): AI generated text
            - mood (str): Current emotional state
            - actions (list): List of actions to execute
    
    Raises:
        APIError: If Gemini API connection fails
        ValidationError: If context format is invalid
    
    Example:
        >>> brain.think("Hello", {"time": "14:30"})
        {'response': 'I see you...', 'mood': 'whispering'}
    """
```

2. **Mevcut fonksiyonlara docstring ekle** (Öncelikli: core/ ve story/)

3. **README.md güncelle**
```markdown
# İlave bölümler ekle:
- 📖 Documentation
  - [Architecture Overview](docs/architecture.md)
  - [API Reference](docs/api.md)
  - [Development Guide](docs/development.md)
  
- 🤝 Contributing
  - [How to Contribute](CONTRIBUTING.md)
  - [Code of Conduct](CODE_OF_CONDUCT.md)
  
- 🐛 Troubleshooting
  - Common issues and solutions
```

---

## 📋 Checklist - İlk 4 Hafta / First 4 Weeks

### Hafta 1: Configuration ✓
- [ ] config.yaml dosyası oluştur
- [ ] ConfigManager sınıfı implement et
- [ ] config.py'yi refactor et
- [ ] Environment variable desteği ekle
- [ ] Test et

### Hafta 2: Error Handling ✓
- [ ] ErrorTracker sınıfı oluştur
- [ ] Kernel'a entegre et
- [ ] Critical error recovery ekle
- [ ] Error log viewer (opsiyonel)
- [ ] Test et

### Hafta 3: Testing ✓
- [ ] pytest kur ve yapılandır
- [ ] Test klasör yapısı oluştur
- [ ] 5+ unit test yaz
- [ ] GitHub Actions CI ekle
- [ ] Coverage raporu oluştur

### Hafta 4: Documentation ✓
- [ ] Docstring standardı seç
- [ ] Core modüllere docstring ekle
- [ ] README.md güncelle
- [ ] CONTRIBUTING.md oluştur
- [ ] API referansı başlat

---

## 🛠️ Kullanışlı Komutlar / Useful Commands

### Development
```bash
# Geliştirme ortamı kur
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Testleri çalıştır
pytest tests/ -v
pytest tests/ --cov=core

# Kod kalitesi kontrolü
flake8 core/ --max-line-length=120
black core/ --check

# Type checking
mypy core/
```

### Git Workflow
```bash
# Yeni feature için branch oluştur
git checkout -b feature/config-system

# Değişiklikleri commit et
git add .
git commit -m "feat: Add configuration management system"

# Push ve PR aç
git push origin feature/config-system
```

---

## 📊 İlerleme Takibi / Progress Tracking

### Her hafta sonunda kontrol et:
```markdown
- [ ] Planlanan özellik tamamlandı mı?
- [ ] Testler yazıldı mı ve geçiyor mu?
- [ ] Dokümantasyon güncellendi mi?
- [ ] Code review yapıldı mı?
- [ ] Performance regresyon var mı?
```

### Başarı Metrikleri
```
Week 1: Config system working + 3 tests
Week 2: Error tracking active + 5 tests
Week 3: 20+ tests passing + CI green
Week 4: 50%+ code documented
```

---

## 🚨 Dikkat Edilmesi Gerekenler / Important Notes

### Yapılacaklar ✅
- Küçük, incremental değişiklikler yap
- Her değişiklikten sonra test et
- Git'te sık commit yap
- Geri dönülebilir değişiklikler yap

### Yapılmayacaklar ❌
- Mevcut working code'u silme
- Büyük refactoring bir anda
- Test etmeden commit
- Breaking changes without migration path

---

## 🆘 Sorun Çözüm / Troubleshooting

### Config yüklenmiyorsa
```python
# Debug: Config dosyasını kontrol et
import yaml
with open('config.yaml') as f:
    print(yaml.safe_load(f))
```

### Testler fail ediyorsa
```bash
# Detaylı output
pytest tests/ -vv -s

# Belirli bir test
pytest tests/unit/test_memory.py::TestMemory::test_store -vv
```

### Import error
```bash
# PYTHONPATH ayarla
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%          # Windows
```

---

## 📚 Kaynaklar / Resources

### Dokümantasyon
- [PyTest Documentation](https://docs.pytest.org/)
- [YAML Specification](https://yaml.org/spec/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### Tools
- **pytest**: Testing framework
- **black**: Code formatter
- **flake8**: Linter
- **mypy**: Type checker
- **coverage.py**: Code coverage

---

## 💬 Feedback ve Sorular / Feedback and Questions

Bu rehberi takip ederken:
- Sorun mu yaşıyorsun? → Issue aç
- Öneri mi var? → Tartışalım
- Başarılı mı tamamladın? → Paylaş!

---

**Son Güncellenme / Last Updated:** 9 Ocak 2026  
**Versiyon / Version:** 1.0  
**Durum / Status:** ✅ Onay Bekliyor / Ready for Review

