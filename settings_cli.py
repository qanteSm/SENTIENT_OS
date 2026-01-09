#!/usr/bin/env python3
"""
SENTIENT_OS Settings Manager CLI

Komut satırı üzerinden ayarları yönetmek için kullanılır.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.settings_manager import settings
from core.achievement_system import achievement_manager


def show_menu():
    """Ana menüyü göster."""
    print("\n" + "="*60)
    print("⚙️  SENTIENT_OS - Ayarlar Yöneticisi")
    print("="*60)
    print()
    print("1. Ayarları Görüntüle")
    print("2. Zorluk Seviyesi Değiştir")
    print("3. Ses Ayarları")
    print("4. Erişilebilirlik Ayarları")
    print("5. Gizlilik Ayarları")
    print("6. Gelişmiş Ayarlar")
    print("7. Başarıları Görüntüle")
    print("8. Ayarları Sıfırla")
    print("9. Çıkış")
    print()
    
    choice = input("Seçiminiz (1-9): ").strip()
    return choice


def show_current_settings():
    """Mevcut ayarları göster."""
    print("\n" + "-"*60)
    print("📋 Mevcut Ayarlar")
    print("-"*60)
    
    print(f"\n🎮 Oyun:")
    print(f"  Zorluk Seviyesi: {settings.get('difficulty', 'normal').upper()}")
    print(f"  Ses Şiddeti: {settings.get('audio_volume', 0.7):.1%}")
    print(f"  Efekt Yoğunluğu: {settings.get('effect_intensity', 1.0):.1f}x")
    print(f"  Dil: {settings.get('language', 'tr').upper()}")
    
    print(f"\n♿ Erişilebilirlik:")
    print(f"  Strobe Efektlerini Devre Dışı Bırak: {settings.get('accessibility.disable_strobe', True)}")
    print(f"  Yüksek Kontrast: {settings.get('accessibility.high_contrast', False)}")
    print(f"  Yavaş Hareket Modu: {settings.get('accessibility.slow_motion', False)}")
    print(f"  Altyazılar: {settings.get('accessibility.subtitles', True)}")
    
    print(f"\n🔒 Gizlilik:")
    print(f"  Streamer Modu: {settings.get('privacy.streamer_mode', True)}")
    print(f"  Analitik: {settings.get('privacy.analytics', False)}")
    
    print(f"\n🔧 Gelişmiş:")
    print(f"  Güvenli Donanım Modu: {settings.get('advanced.safe_hardware', False)}")
    print(f"  Kaos Seviyesi: {settings.get('advanced.chaos_level', 0)}/10")
    print(f"  Mock Modu: {settings.get('advanced.mock_mode', False)}")
    
    print("-"*60)


def change_difficulty():
    """Zorluk seviyesi değiştir."""
    print("\n🎮 Zorluk Seviyesi:")
    print("  1. Kolay (0.5x efekt)")
    print("  2. Normal (1.0x efekt)")
    print("  3. Zor (1.5x efekt)")
    print("  4. Extreme (2.0x efekt)")
    
    choice = input("\nSeçim (1-4): ").strip()
    
    difficulty_map = {
        "1": "easy",
        "2": "normal",
        "3": "hard",
        "4": "extreme"
    }
    
    if choice in difficulty_map:
        settings.set("difficulty", difficulty_map[choice])
        print(f"✅ Zorluk seviyesi '{difficulty_map[choice]}' olarak ayarlandı.")
    else:
        print("❌ Geçersiz seçim!")


def change_audio():
    """Ses ayarları."""
    print("\n🔊 Ses Ayarları:")
    
    try:
        volume = float(input("Ses şiddeti (0.0 - 1.0): ").strip())
        if 0.0 <= volume <= 1.0:
            settings.set("audio_volume", volume)
            print(f"✅ Ses şiddeti {volume:.1%} olarak ayarlandı.")
        else:
            print("❌ Değer 0.0 ile 1.0 arasında olmalı!")
    except ValueError:
        print("❌ Geçersiz değer!")


def change_accessibility():
    """Erişilebilirlik ayarları."""
    print("\n♿ Erişilebilirlik Ayarları:")
    print("  1. Strobe Efektlerini Devre Dışı Bırak")
    print("  2. Yüksek Kontrast Modu")
    print("  3. Yavaş Hareket Modu")
    print("  4. Altyazıları Aç/Kapat")
    print("  5. Geri")
    
    choice = input("\nSeçim (1-5): ").strip()
    
    if choice == "1":
        current = settings.get('accessibility.disable_strobe', True)
        settings.set('accessibility.disable_strobe', not current)
        print(f"✅ Strobe koruması: {not current}")
    elif choice == "2":
        current = settings.get('accessibility.high_contrast', False)
        settings.set('accessibility.high_contrast', not current)
        print(f"✅ Yüksek kontrast: {not current}")
    elif choice == "3":
        current = settings.get('accessibility.slow_motion', False)
        settings.set('accessibility.slow_motion', not current)
        print(f"✅ Yavaş hareket: {not current}")
    elif choice == "4":
        current = settings.get('accessibility.subtitles', True)
        settings.set('accessibility.subtitles', not current)
        print(f"✅ Altyazılar: {not current}")


def change_privacy():
    """Gizlilik ayarları."""
    print("\n🔒 Gizlilik Ayarları:")
    print("  1. Streamer Modu")
    print("  2. Analitik (Anonim kullanım istatistikleri)")
    print("  3. Geri")
    
    choice = input("\nSeçim (1-3): ").strip()
    
    if choice == "1":
        current = settings.get('privacy.streamer_mode', True)
        settings.set('privacy.streamer_mode', not current)
        print(f"✅ Streamer modu: {not current}")
    elif choice == "2":
        current = settings.get('privacy.analytics', False)
        settings.set('privacy.analytics', not current)
        print(f"✅ Analitik: {not current}")


def change_advanced():
    """Gelişmiş ayarlar."""
    print("\n🔧 Gelişmiş Ayarlar:")
    print("  1. Güvenli Donanım Modu")
    print("  2. Kaos Seviyesi (0-10)")
    print("  3. Mock Modu")
    print("  4. Geri")
    
    choice = input("\nSeçim (1-4): ").strip()
    
    if choice == "1":
        current = settings.get('advanced.safe_hardware', False)
        settings.set('advanced.safe_hardware', not current)
        print(f"✅ Güvenli donanım modu: {not current}")
    elif choice == "2":
        try:
            level = int(input("Kaos seviyesi (0-10): ").strip())
            if 0 <= level <= 10:
                settings.set('advanced.chaos_level', level)
                print(f"✅ Kaos seviyesi: {level}/10")
            else:
                print("❌ Değer 0 ile 10 arasında olmalı!")
        except ValueError:
            print("❌ Geçersiz değer!")
    elif choice == "3":
        current = settings.get('advanced.mock_mode', False)
        settings.set('advanced.mock_mode', not current)
        print(f"✅ Mock modu: {not current}")


def show_achievements():
    """Başarıları göster."""
    print("\n" + "-"*60)
    print("🏆 Başarılar")
    print("-"*60)
    
    unlocked = achievement_manager.get_unlocked_achievements()
    locked = achievement_manager.get_locked_achievements()
    total = len(achievement_manager.achievements)
    points = achievement_manager.get_total_points()
    completion = achievement_manager.get_completion_percentage()
    
    print(f"\nİlerleme: {len(unlocked)}/{total} ({completion:.1f}%)")
    print(f"Toplam Puan: {points}")
    
    if unlocked:
        print(f"\n✅ Açılmış Başarılar ({len(unlocked)}):")
        for ach in sorted(unlocked, key=lambda a: a.unlock_time or ""):
            time_str = ach.unlock_time[:10] if ach.unlock_time else "?"
            print(f"  🏆 {ach.name} - {ach.description} (+{ach.points}) [{time_str}]")
    
    if locked:
        print(f"\n🔒 Kilitli Başarılar ({len(locked)}):")
        for ach in locked[:10]:  # Show first 10
            print(f"  🔒 {ach.name} - {ach.description} (+{ach.points})")
        
        if len(locked) > 10:
            print(f"  ... ve {len(locked) - 10} tane daha")
    
    print("-"*60)


def reset_settings():
    """Ayarları sıfırla."""
    print("\n⚠️  UYARI: Tüm ayarlar varsayılanlara dönecek!")
    confirm = input("Devam etmek istediğinizden emin misiniz? (evet/hayır): ").strip().lower()
    
    if confirm in ['evet', 'e', 'yes', 'y']:
        settings.reset_to_defaults()
        print("✅ Ayarlar sıfırlandı.")
    else:
        print("❌ İptal edildi.")


def main():
    """Ana program döngüsü."""
    print("\n🤖 SENTIENT_OS Ayarlar Yöneticisi'ne Hoş Geldiniz!")
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            show_current_settings()
        elif choice == "2":
            change_difficulty()
        elif choice == "3":
            change_audio()
        elif choice == "4":
            change_accessibility()
        elif choice == "5":
            change_privacy()
        elif choice == "6":
            change_advanced()
        elif choice == "7":
            show_achievements()
        elif choice == "8":
            reset_settings()
        elif choice == "9":
            print("\n👋 Çıkış yapılıyor...")
            break
        else:
            print("❌ Geçersiz seçim!")
        
        input("\nDevam etmek için Enter'a basın...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Güvenli çıkış yapıldı.")
        sys.exit(0)
