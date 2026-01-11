# Scripts Directory

Bu klasör, SENTIENT_OS projesinin geliştirme ve debug süreçlerinde kullanılan yardımcı scriptleri içerir.

## 📁 Klasör Yapısı

### `debug/`
Hata ayıklama ve debug scriptleri:
- `debug_direct_id.py` - Direct input debugging
- `debug_dispatcher.py` - Dispatcher action testing
- `debug_isolated.py` - Isolated component testing
- `debug_sapi.py` - SAPI voice debugging
- `debug_voices.py` - TTS voice enumeration
- `debug_onecore.ps1` - PowerShell OneCore voice debugging

### `utils/`
Kurulum, düzeltme ve doğrulama araçları:
- `fix_config.py` - Config dosyası onarımı
- `fix_voices.py` - TTS voice sistemi düzeltme
- `create_infrasound.py` - Infrasound dalga formu oluşturma
- `verify_drone_audio.py` - Drone audio sistemi doğrulama
- `verify_enhancements.py` - Phase enhancements testi
- `speak_to_file.ps1` - PowerShell TTS to file

### `tests/`
Manuel ve integration test scriptleri:
- `test_chat.py` - Chat sistemi testi
- `test_chat_minimal.py` - Minimal chat testi
- `test_core_v2.py` - Core v2 sistem testi
- `test_watchdog_gameplay.py` - Watchdog gameplay integration testi
- `quick_test.py` - Hızlı sistem testi

## 🚀 Kullanım

### Debug Testi
```bash
python scripts/debug/debug_dispatcher.py
```

### Ses Sistemi Kontrolü
```bash
python scripts/utils/verify_drone_audio.py
```

### Integration Test
```bash
python scripts/tests/test_watchdog_gameplay.py
```

## 📝 Notlar

- Bu scriptler **geliştirme amaçlı**dır - production'da çalıştırılmamalı
- Bazı scriptler sistem kaynaklarına erişim gerektirir (mikrofon, TTS)
- Test scriptleri genelde PyQt6 event loop başlatır

## 🧹 Temizlik

Kullanılmayan veya eski scriptler periyodik olarak temizlenmelidir.
