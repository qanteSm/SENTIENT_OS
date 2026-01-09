#!/usr/bin/env python3
"""
SENTIENT_OS Diagnostic Tool

Sistem durumunu kontrol eder ve sorunları tespit eder.
"""

import sys
import os
import platform
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config


def check_python_version():
    """Python versiyonunu kontrol et."""
    version = sys.version_info
    print(f"\n🐍 Python Versiyonu: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ❌ UYARI: Python 3.8+ gerekli!")
        return False
    else:
        print("  ✅ Python versiyonu uygun")
        return True


def check_dependencies():
    """Gerekli kütüphaneleri kontrol et."""
    print("\n📦 Bağımlılık Kontrolü:")
    
    required_packages = [
        ('PyQt6', 'PyQt6'),
        ('google.generativeai', 'google-generativeai'),
        ('pygame', 'pygame'),
        ('pyttsx3', 'pyttsx3'),
        ('psutil', 'psutil'),
        ('requests', 'requests'),
        ('PIL', 'pillow'),
        ('cryptography', 'cryptography'),
    ]
    
    all_ok = True
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} - EKSİK!")
            all_ok = False
    
    if not all_ok:
        print("\n  Eksik paketleri yüklemek için:")
        print("  pip install -r requirements.txt")
    
    return all_ok


def check_platform():
    """Platform bilgilerini göster."""
    print(f"\n💻 Platform Bilgileri:")
    print(f"  İşletim Sistemi: {platform.system()} {platform.release()}")
    print(f"  Mimari: {platform.machine()}")
    print(f"  Python İmplementasyonu: {platform.python_implementation()}")
    
    if Config.IS_WINDOWS:
        print("  ✅ Windows tespit edildi (Tam özellik desteği)")
    else:
        print("  ⚠️  Windows dışı sistem (Mock mode aktif)")
    
    return True


def check_api_key():
    """Gemini API anahtarını kontrol et."""
    print(f"\n🔑 API Anahtarı Kontrolü:")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"  ✅ API anahtarı bulundu (uzunluk: {len(api_key)})")
        return True
    else:
        print("  ⚠️  API anahtarı bulunamadı")
        print("  Mock mode kullanılacak (sınırlı özellikler)")
        return False


def check_directories():
    """Gerekli dizinleri kontrol et."""
    print(f"\n📁 Dizin Kontrolü:")
    
    directories = [
        Config.LOGS_DIR,
        Config.CACHE_DIR,
        Config.LOCALES_DIR,
    ]
    
    all_ok = True
    for directory in directories:
        if os.path.exists(directory):
            print(f"  ✅ {directory}")
        else:
            print(f"  ⚠️  {directory} - Oluşturuluyor...")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"     ✅ Oluşturuldu")
            except Exception as e:
                print(f"     ❌ Hata: {e}")
                all_ok = False
    
    return all_ok


def check_permissions():
    """Dosya yazma izinlerini kontrol et."""
    print(f"\n🔐 İzin Kontrolü:")
    
    test_file = os.path.join(Config.BASE_DIR, ".permission_test")
    
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("  ✅ Yazma izinleri tamam")
        return True
    except Exception as e:
        print(f"  ❌ Yazma izni hatası: {e}")
        return False


def check_config():
    """Config ayarlarını göster."""
    print(f"\n⚙️  Yapılandırma:")
    print(f"  App Name: {Config.APP_NAME}")
    print(f"  Version: {Config.VERSION}")
    print(f"  Language: {Config.LANGUAGE}")
    print(f"  Streamer Mode: {Config.STREAMER_MODE}")
    print(f"  AI Safety Check: {Config.AI_SAFETY_CHECK}")
    print(f"  Safe Hardware: {Config.SAFE_HARDWARE}")
    print(f"  Chaos Level: {Config.CHAOS_LEVEL}")
    print(f"  Enable Strobe: {Config.ENABLE_STROBE}")
    print(f"  Mock Mode: {Config.IS_MOCK}")
    
    return True


def check_memory_file():
    """Hafıza dosyasını kontrol et."""
    print(f"\n🧠 Hafıza Dosyası:")
    
    memory_file = os.path.join(Config.BASE_DIR, "brain_dump.json")
    
    if os.path.exists(memory_file):
        size = os.path.getsize(memory_file)
        print(f"  ✅ brain_dump.json mevcut ({size} bytes)")
        return True
    else:
        print("  ℹ️  brain_dump.json yok (ilk çalıştırmada oluşturulacak)")
        return True


def check_settings_file():
    """Ayarlar dosyasını kontrol et."""
    print(f"\n⚙️  Ayarlar Dosyası:")
    
    settings_file = os.path.join(Config.BASE_DIR, "user_settings.json")
    
    if os.path.exists(settings_file):
        size = os.path.getsize(settings_file)
        print(f"  ✅ user_settings.json mevcut ({size} bytes)")
    else:
        print("  ℹ️  user_settings.json yok (varsayılanlar kullanılacak)")
    
    return True


def run_full_diagnostic():
    """Tüm diagnostikleri çalıştır."""
    print("="*70)
    print("🔍 SENTIENT_OS - Sistem Tanılaması")
    print("="*70)
    
    checks = [
        ("Python Versiyonu", check_python_version),
        ("Platform", check_platform),
        ("Bağımlılıklar", check_dependencies),
        ("API Anahtarı", check_api_key),
        ("Dizinler", check_directories),
        ("İzinler", check_permissions),
        ("Yapılandırma", check_config),
        ("Hafıza Dosyası", check_memory_file),
        ("Ayarlar Dosyası", check_settings_file),
    ]
    
    results = {}
    
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ {name} kontrolü sırasında hata: {e}")
            results[name] = False
    
    # Özet
    print("\n" + "="*70)
    print("📊 ÖZET")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print(f"\nSonuç: {passed}/{total} kontrol başarılı")
    
    if passed == total:
        print("\n✅ Sistem hazır! 'python main.py' ile başlatabilirsiniz.")
        return 0
    elif passed >= total * 0.7:
        print("\n⚠️  Bazı sorunlar var ama sistem çalışabilir.")
        return 0
    else:
        print("\n❌ Kritik sorunlar tespit edildi. Lütfen yukarıdaki hataları düzeltin.")
        return 1


def show_quick_help():
    """Hızlı yardım göster."""
    print("\n" + "="*70)
    print("❓ Hızlı Yardım")
    print("="*70)
    print("\n🚀 Başlatma:")
    print("  python main.py")
    print("\n⚙️  Ayarlar:")
    print("  python settings_cli.py")
    print("\n🔍 Tanılama:")
    print("  python diagnostic.py")
    print("\n📝 Test:")
    print("  python test_chat.py")
    print("\n📚 Dokümantasyon:")
    print("  README.md - Genel bilgiler")
    print("  CONTRIBUTING.md - Katkıda bulunma")
    print("  ARCHITECTURE.md - Teknik detaylar")
    print("\n🔗 Bağlantılar:")
    print("  GitHub: https://github.com/qanteSm/SENTIENT_OS")
    print("  Issues: https://github.com/qanteSm/SENTIENT_OS/issues")
    print("="*70)


def main():
    """Ana program."""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_quick_help()
        return 0
    
    exit_code = run_full_diagnostic()
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-v', '--verbose', 'help']:
        show_quick_help()
    
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 İptal edildi.")
        sys.exit(0)
