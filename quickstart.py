#!/usr/bin/env python3
"""
SENTIENT_OS Quick Start Script

Yeni kullanıcılar için hızlı kurulum ve başlatma scripti.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def print_banner():
    """Hoş geldin banneri."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              SENTIENT_OS - Hızlı Başlangıç               ║
║                      Version 4.1                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

def check_python():
    """Python versiyonunu kontrol et."""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro} tespit edildi")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ HATA: Python 3.8 veya üzeri gerekli!")
        print("   https://www.python.org/downloads/ adresinden indirebilirsiniz.")
        return False
    
    print("✅ Python versiyonu uygun\n")
    return True

def install_dependencies():
    """Bağımlılıkları yükle."""
    print("📦 Bağımlılıklar kuruluyor...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✅ Bağımlılıklar başarıyla kuruldu\n")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Bağımlılık kurulumu başarısız!")
        print("   Manuel olarak kurmayı deneyin: pip install -r requirements.txt")
        return False

def setup_api_key():
    """API anahtarını yapılandır."""
    print("🔑 Gemini API Anahtarı Kurulumu")
    print("-" * 60)
    
    current_key = os.getenv("GEMINI_API_KEY")
    
    if current_key:
        print(f"✅ Mevcut API anahtarı bulundu (uzunluk: {len(current_key)})")
        change = input("   Değiştirmek ister misiniz? (e/h): ").strip().lower()
        if change not in ['e', 'evet', 'y', 'yes']:
            print()
            return True
    
    print("\nGemini API anahtarınızı girin:")
    print("(https://makersuite.google.com/app/apikey adresinden alabilirsiniz)")
    print("Atlamak için boş bırakın (Mock mode kullanılır)")
    
    api_key = input("\nAPI Key: ").strip()
    
    if not api_key:
        print("⚠️  API anahtarı girilmedi. Mock mode kullanılacak.")
        print("   (Sınırlı özelliklerle çalışır)\n")
        return True
    
    # .env dosyasına kaydet
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    
    try:
        with open(env_file, 'w') as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        print("✅ API anahtarı kaydedildi\n")
        return True
    except Exception as e:
        print(f"❌ API anahtarı kaydedilemedi: {e}")
        print("   Manuel olarak .env dosyası oluşturabilirsiniz.\n")
        return False

def create_directories():
    """Gerekli dizinleri oluştur."""
    print("📁 Dizinler oluşturuluyor...")
    
    dirs = ["logs", "cache", "locales"]
    
    for dir_name in dirs:
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        os.makedirs(dir_path, exist_ok=True)
        print(f"   ✅ {dir_name}/")
    
    print()

def run_diagnostic():
    """Sistem tanılaması çalıştır."""
    print("🔍 Sistem tanılaması çalıştırılıyor...\n")
    print("=" * 60)
    
    try:
        subprocess.check_call([sys.executable, "diagnostic.py"])
        return True
    except subprocess.CalledProcessError:
        print("\n⚠️  Tanılama bazı sorunlar tespit etti.")
        return False

def configure_settings():
    """İlk ayarları yapılandır."""
    print("\n⚙️  Ayarlar Yapılandırması")
    print("-" * 60)
    print("Varsayılan ayarları kullanmak ister misiniz? (Önerilir)")
    
    choice = input("(e/h): ").strip().lower()
    
    if choice in ['h', 'hayır', 'n', 'no']:
        print("\nAyarlar menüsü açılıyor...")
        try:
            subprocess.call([sys.executable, "settings_cli.py"])
        except:
            print("⚠️  Ayarlar aracı çalıştırılamadı. Manuel açın: python settings_cli.py")
    else:
        print("✅ Varsayılan ayarlar kullanılacak")
        # Create default settings
        from core.settings_manager import settings
        settings.save_settings()
    
    print()

def show_final_instructions():
    """Son talimatları göster."""
    print("\n" + "=" * 60)
    print("🎉 Kurulum Tamamlandı!")
    print("=" * 60)
    print("\n📖 Başlatma Komutları:")
    print("   python main.py              - Programı başlat")
    print("   python settings_cli.py      - Ayarları düzenle")
    print("   python diagnostic.py        - Sistem durumunu kontrol et")
    print("\n📚 Dokümantasyon:")
    print("   README.md                   - Genel bilgiler")
    print("   CONTRIBUTING.md             - Katkıda bulunma")
    print("   ARCHITECTURE.md             - Teknik detaylar")
    print("\n⚠️  UYARI:")
    print("   Bu program korku deneyimi için tasarlanmıştır.")
    print("   Epilepsi veya ışık hassasiyeti varsa KULLANMAYIN!")
    print("\n🔗 Destek:")
    print("   GitHub: https://github.com/qanteSm/SENTIENT_OS/issues")
    print("\n" + "=" * 60)
    print("\nProgramı başlatmak ister misiniz? (e/h): ", end='')
    
    choice = input().strip().lower()
    
    if choice in ['e', 'evet', 'y', 'yes']:
        print("\n🚀 SENTIENT_OS başlatılıyor...\n")
        try:
            subprocess.call([sys.executable, "main.py"])
        except KeyboardInterrupt:
            print("\n\n👋 İptal edildi.")
        except Exception as e:
            print(f"\n❌ Başlatma hatası: {e}")
            print("   Manuel başlatmayı deneyin: python main.py")
    else:
        print("\n✅ Hazırsınız! 'python main.py' ile başlatabilirsiniz.")

def main():
    """Ana kurulum akışı."""
    print_banner()
    
    print("Bu script, SENTIENT_OS'i ilk kez kullanacaklar için")
    print("otomatik kurulum ve yapılandırma yapar.\n")
    
    # 1. Python kontrolü
    if not check_python():
        return 1
    
    # 2. Bağımlılıkları yükle
    print("Bağımlılıkları yüklemek istiyor musunuz? (e/h): ", end='')
    if input().strip().lower() in ['e', 'evet', 'y', 'yes']:
        if not install_dependencies():
            print("\n⚠️  Devam etmek istiyor musunuz? (e/h): ", end='')
            if input().strip().lower() not in ['e', 'evet', 'y', 'yes']:
                return 1
    
    # 3. Dizinleri oluştur
    create_directories()
    
    # 4. API anahtarını yapılandır
    setup_api_key()
    
    # 5. Sistem tanılaması
    print("Sistem tanılaması çalıştırılsın mı? (e/h): ", end='')
    if input().strip().lower() in ['e', 'evet', 'y', 'yes']:
        run_diagnostic()
    
    # 6. Ayarları yapılandır
    configure_settings()
    
    # 7. Son talimatlar
    show_final_instructions()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Kurulum iptal edildi.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        print("   Lütfen manuel kurulum yapın.")
        sys.exit(1)
