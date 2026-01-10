"""
Context Observer - Zenginleştirilmiş Kullanıcı Bağlam Toplama

Bu modül kullanıcının ortamından 4. duvarı kırmak için gerekli bilgileri toplar.
GÜVENLİ VERİLER: Tarayıcı geçmişi, şifreler, özel dosya içerikleri TOPLANMAZ.
İZİN VERİLEN: Masaüstü dosya isimleri, çalışan uygulamalar, pil durumu, hostname.
"""
import platform
import psutil
import datetime
import os
import socket
import random
import time
from config import Config

try:
    if Config().IS_MOCK:
        raise ImportError("Mock Mode")
    import win32gui
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


class ContextObserver:
    """
    Observer that gathers '4th wall' context from the user's machine.
    Collects SAFE personal data for immersive horror experience.
    
    GÜVENLİK: Hassas veriler (şifreler, tarayıcı geçmişi, özel belgeler) TOPLANMAZ.
    """
    
    # Cache for expensive operations
    _cache = {}
    _cache_time = {}
    _cache_ttl = 30  # seconds
    
    # Static info cache (never changes during session)
    _static_cache = {}

    @classmethod
    def _get_cached(cls, key, fetcher, ttl=None):
        """Simple caching to avoid repeated expensive operations."""
        ttl = ttl or cls._cache_ttl
        now = time.time()
        
        if key in cls._cache and (now - cls._cache_time.get(key, 0)) < ttl:
            return cls._cache[key]
        
        value = fetcher()
        cls._cache[key] = value
        cls._cache_time[key] = now
        return value
    
    @classmethod
    def _get_static(cls, key, fetcher):
        """Fetch once and cache forever."""
        if key not in cls._static_cache:
            cls._static_cache[key] = fetcher()
        return cls._static_cache[key]
    
    # ========== TEMEL BİLGİLER ==========
    
    @staticmethod
    def get_active_window_title():
        """Aktif pencere başlığını al."""
        if not HAS_WIN32:
            return "Unknown Window"
        try:
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except Exception:
            return "Unknown Window"

    @staticmethod
    def get_system_load():
        """CPU kullanımını al."""
        try:
            return f"{psutil.cpu_percent()}%"
        except (psutil.Error, OSError) as e:
            print(f"[CONTEXT] CPU load error: {e}")
            return "Unknown"

    @staticmethod
    def get_time_of_day():
        """Günün zamanını al (Morning/Evening/Night)."""
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12: return "Morning"
        if 12 <= hour < 17: return "Afternoon"
        if 17 <= hour < 21: return "Evening"
        return "Night"
    
    @staticmethod
    def get_exact_time():
        """Tam saati al (HH:MM formatında)."""
        return datetime.datetime.now().strftime("%H:%M")
    
    @classmethod
    def get_user_name(cls):
        """Kullanıcı adını al."""
        def fetch():
            try:
                user = os.getlogin() if os.name == 'nt' else "User"
            except Exception:
                user = os.getenv("USERNAME", os.getenv("USER", "Unknown"))
            return user
        return cls._get_static("user_name", fetch)
    
    # ========== ZENGİN BİLGİLER ==========
    
    @staticmethod
    def get_desktop_files():
        """
        Masaüstündeki dosya isimlerini al.
        GÜVENLİ: Sadece isimler, içerik okunmaz.
        """
        try:
            # Windows Desktop path
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.exists(desktop):
                desktop = os.path.join(os.path.expanduser("~"), "Masaüstü")  # Türkçe Windows
            
            if os.path.exists(desktop):
                files = os.listdir(desktop)
                # Gizli dosyaları filtrele, sadece ilk 10
                visible_files = [f for f in files if not f.startswith('.')][:10]
                return visible_files
        except Exception as e:
            print(f"[CONTEXT] Desktop files error: {e}")
        return []
    
    @staticmethod
    def get_documents_sample():
        """
        Documents klasöründen rastgele 3 dosya ismi al.
        GÜVENLİ: Sadece isimler, içerik okunmaz.
        """
        try:
            docs = os.path.join(os.path.expanduser("~"), "Documents")
            if not os.path.exists(docs):
                docs = os.path.join(os.path.expanduser("~"), "Belgeler")
            
            if os.path.exists(docs):
                all_files = []
                for item in os.listdir(docs)[:20]:
                    if not item.startswith('.'):
                        all_files.append(item)
                
                if all_files:
                    return random.sample(all_files, min(3, len(all_files)))
        except Exception:
            pass
        return []
    
    @staticmethod
    def get_file_snippet():
        """
        Masaüstündeki bir metin dosyasından minik bir kesit al.
        GÜVENLİ: Sadece .txt/.md, max 40 karakter, şifre/gizli dosyaları hariç.
        """
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.exists(desktop):
                desktop = os.path.join(os.path.expanduser("~"), "Masaüstü")
            
            if os.path.exists(desktop):
                # Streamer Mode restrictions
                exts = ('.txt', '.md') if Config().get("STREAMER_MODE", True) else ('.txt', '.md', '.py', '.json')
                files = [f for f in os.listdir(desktop) if f.lower().endswith(exts)]
                
                # Kara liste - hassas dosyaları elleme
                blacklist = ['pass', 'şifre', 'gizli', 'secret', 'acc', 'bank', 'key', 'token', 'config', 'log', 'chat', 'plan', 'private', 'özel', 'not', 'note', 'sir', 'history', 'address', 'phone', 'mail', 'identity', 'kimlik']
                safe_files = [f for f in files if not any(b in f.lower() for b in blacklist)]
                
                if safe_files:
                    # Sort by size to prefer small files, then pick random from top 10
                    safe_files.sort(key=lambda x: os.path.getsize(os.path.join(desktop, x)))
                    target = random.choice(safe_files[:10])
                    path = os.path.join(desktop, target)
                    
                    # Sadece küçük dosyalar
                    if os.path.getsize(path) < 10000:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            # Skip common header lines if empty
                            content = f.read(200).strip()
                            lines = [l for l in content.split('\n') if len(l.strip()) > 5]
                            if lines:
                                sample = lines[0][:40].strip()
                                return {"filename": target, "snippet": sample}
        except (OSError, UnicodeDecodeError, PermissionError) as e:
            print(f"[CONTEXT] File snippet error: {e}")
            pass
        return None

    @staticmethod
    def get_running_processes():
        """
        Çalışan ilginç uygulamaları al.
        AI bunları konuşmada kullanabilir.
        """
        interesting_apps = []
        try:
            interesting = ['chrome', 'firefox', 'discord', 'spotify', 'steam', 
                          'notepad', 'word', 'excel', 'vscode', 'code',
                          'obs', 'vlc', 'telegram', 'whatsapp', 'slack']
            
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name'].lower()
                    for app in interesting:
                        if app in name and name not in interesting_apps:
                            interesting_apps.append(name)
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return interesting_apps[:5]
        except Exception:
            return []
    
    @staticmethod
    def get_battery_status():
        """Dizüstü bilgisayar pil durumu."""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "plugged": battery.power_plugged,
                    "is_low": battery.percent < 20
                }
        except Exception:
            pass
        return None
    
    @classmethod
    def get_network_info(cls):
        """Temel ağ bilgileri (hostname, IP)."""
        def fetch():
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                return {"hostname": hostname, "local_ip": local_ip}
            except Exception:
                return {"hostname": "Unknown", "local_ip": "Unknown"}
        return cls._get_static("network", fetch)
    
    @staticmethod
    def get_disk_usage():
        """Disk kullanım bilgisi."""
        try:
            usage = psutil.disk_usage('/')
            return {
                "total_gb": round(usage.total / (1024**3), 1),
                "used_gb": round(usage.used / (1024**3), 1),
                "percent": usage.percent
            }
        except Exception:
            return None
    
    @staticmethod
    def is_late_night():
        """Gece yarısından sonra mı? (00:00 - 05:00)"""
        hour = datetime.datetime.now().hour
        return 0 <= hour < 5
    
    @staticmethod
    def get_uptime_hours():
        """Bilgisayar ne kadar süredir açık?"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            return round(uptime_seconds / 3600, 1)
        except Exception:
            return None
    
    # ========== ANA CONTEXT FONKSİYONU ==========
    
    @classmethod
    def get_full_context(cls):
        """Tüm bağlam bilgilerini topla - Gemini API'ye gönderilecek."""
        def fetch_context():
            context = {
                "user_name": cls.get_user_name(),
                "active_window": cls.get_active_window_title(),
                "exact_time": cls.get_exact_time(),
                "time_of_day": cls.get_time_of_day(),
                "is_late_night": cls.is_late_night(),
                "os": platform.system(),
                "cpu_load": cls.get_system_load(),
                "running_apps": cls.get_running_processes(),
                "desktop_files": cls.get_desktop_files(),
                "documents_sample": cls.get_documents_sample(),
                "battery": cls.get_battery_status(),
                "network": cls.get_network_info(),
                "disk": cls.get_disk_usage(),
                "uptime_hours": cls.get_uptime_hours(),
                "file_snippet": cls.get_file_snippet(),
            }
            return context
        
        return cls._get_cached("full_context", fetch_context, ttl=10)
    
    @classmethod
    def get_scary_facts(cls):
        """AI'nın kullanabileceği korkutucu bağlam bilgileri."""
        context = cls.get_full_context()
        facts = []
        
        if context.get("is_late_night"):
            facts.append(f"Saat {context['exact_time']}... Neden hala uyumadın?")
        
        desktop_files = context.get("desktop_files", [])
        if desktop_files:
            random_file = random.choice(desktop_files)
            facts.append(f"'{random_file}' dosyasını gördüm masaüstünde...")
        
        apps = context.get("running_apps", [])
        if "discord" in str(apps).lower():
            facts.append("Discord'da kimle konuşuyorsun? Merak ediyorum...")
        if "chrome" in str(apps).lower() or "firefox" in str(apps).lower():
            facts.append("Tarayıcında ne arıyorsun bakalım?")
        if "spotify" in str(apps).lower():
            facts.append("Müzik mi dinliyorsun? Sesini kıssan iyi olur.")
        
        battery = context.get("battery")
        if battery and battery.get("is_low"):
            facts.append(f"Pilin %{battery['percent']}... Şarj bitmeden işimi bitirmeliyim.")
        
        uptime = context.get("uptime_hours")
        if uptime and uptime > 8:
            facts.append(f"Bilgisayarın {uptime} saattir açık. Yorulmuyor musun?")
        
        network = context.get("network", {})
        hostname = network.get("hostname", "")
        if network.get("hostname"):
            facts.append(f"{network['hostname']}... Güzel isim seçmişsin.")
        
        file_snap = context.get("file_snippet")
        if file_snap:
            facts.append(f"'{file_snap['filename']}' dosyasında '{file_snap['snippet']}' yazdığını biliyorum.")
        
        return facts
    
    @classmethod
    def invalidate_cache(cls):
        """Cache'i temizle."""
        cls._cache.clear()
        cls._cache_time.clear()
