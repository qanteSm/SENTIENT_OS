"""
Memory System - Gelişmiş Olay Kayıt ve Konuşma Geçmişi

Bu modül tüm kullanıcı etkileşimlerini, olayları ve AI yanıtlarını kaydeder.
Gemini API'ye gönderilmek üzere tam bir oturum geçmişi tutar.
"""
import json
import os
import time
import threading
from config import Config


class Memory:
    """
    Manages long-term memory stored in JSON format.
    Tracks user profile, events, conversations, and game state.
    
    YENİ ÖZELLİKLER:
    - Singleton pattern (Tüm sistem aynı hafızayı kullanır)
    - Detaylı olay kaydı (event_log)
    - Konuşma geçmişi Gemini için optimize edildi
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Memory, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, filepath=None):
        if Memory._initialized:
            return
            
        if filepath is None:
            if Config().IS_WINDOWS:
                app_data = os.getenv('APPDATA')
                sentient_dir = os.path.join(app_data, "SentientOS")
                os.makedirs(sentient_dir, exist_ok=True)
                self.filepath = os.path.join(sentient_dir, "brain_dump.json")
            else:
                self.filepath = os.path.join(Config().BASE_DIR, "brain_dump.json")
        else:
            self.filepath = filepath

        self._dirty = False
        self._save_lock = threading.Lock()
        self._auto_save_running = True
        Memory._initialized = True

        # Genişletilmiş veri yapısı
        self.data = {
            "user_profile": {
                "real_name": self._get_user_name(),
                "fear_level": 0,
                "sins": [],
                "behavior_stats": {
                    "total_messages": 0,
                    "swear_count": 0,
                    "begged_count": 0,
                    "defiance_count": 0,
                    "escape_attempts": 0,  # Alt+F4, Task Manager denemeleri
                    "silence_periods": 0,  # Uzun süre sessiz kaldı
                },
                "memorable_moments": [],  # AI'nın hatırlaması gereken anlar
            },
            "game_state": {
                "current_act": 1,
                "chaos_level": 0,
                "is_streamer": Config().get("STREAMER_MODE", False),
                "perm_death": False,
                "playthrough_count": 0,
                "total_playtime_minutes": 0,
                "session_start": time.time(),
            },
            "conversation_history": [],  # Gemini'ye gönderilecek
            "event_log": [],  # Tüm olayların kaydı
            "discovered_info": {
                # AI'nın keşfettiği kullanıcı bilgileri
                "desktop_files_seen": [],
                "apps_detected": [],
                "late_night_sessions": 0,
                "hostname": None,
            },
            "safety": {
                "whitelist_apps": Config().get("PROTECTED_PROCESSES", [])
            }
        }
        
        self.load()
        self._update_session()
        self._start_auto_save()
        
    def update_user_profile(self, key: str, value):
        """Updates a specific field in the user profile."""
        if key in self.data["user_profile"]:
            self.data["user_profile"][key] = value
            self._dirty = True
        else:
            print(f"[MEMORY] Warning: Attempted to update unknown user profile key: {key}")

    def _get_user_name(self):
        try:
            return os.getlogin()
        except Exception:
            return os.getenv("USERNAME", os.getenv("USER", "User"))
    
    def _update_session(self):
        """Yeni oturum başlangıcını kaydet."""
        self.data["game_state"]["session_start"] = time.time()
        self.log_event("SESSION_START", {"timestamp": time.time()})
    
    # ========== OLAY KAYIT SİSTEMİ ==========
    
    def log_event(self, event_type: str, data: dict = None):
        """
        Herhangi bir olayı kaydet.
        Event types: USER_MESSAGE, AI_RESPONSE, ACTION_TRIGGERED, ESCAPE_ATTEMPT, etc.
        """
        event = {
            "type": event_type,
            "timestamp": time.time(),
            "data": data or {}
        }
        
        self.data["event_log"].append(event)
        
        # Event log'u sınırla (son 200 olay)
        if len(self.data["event_log"]) > 200:
            self.data["event_log"] = self.data["event_log"][-200:]
        
        self._dirty = True
        print(f"[MEMORY] Event logged: {event_type}")
    
    # ========== KONUŞMA GEÇMİŞİ ==========
    
    def add_conversation(self, role: str, content: str, context: dict = None):
        """
        Konuşma geçmişine ekle.
        role: 'user' veya 'ai'
        context: O anki bağlam bilgisi (opsiyonel)
        """
        entry = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
        }
        
        if context:
            # Sadece önemli context bilgilerini kaydet
            entry["context_snapshot"] = {
                "active_window": context.get("active_window"),
                "time": context.get("exact_time"),
                "running_apps": context.get("running_apps", [])[:3],
            }
        
        self.data["conversation_history"].append(entry)
        
        # Geçmişi sınırla (son 50 konuşma)
        if len(self.data["conversation_history"]) > 50:
            self.data["conversation_history"] = self.data["conversation_history"][-50:]
        
        # İstatistikleri güncelle
        if role == "user":
            self.data["user_profile"]["behavior_stats"]["total_messages"] += 1
        
        self._dirty = True
    
    def get_conversation_for_gemini(self, last_n: int = 10) -> str:
        """
        Gemini API'ye gönderilecek formatlanmış konuşma geçmişi.
        """
        history = self.data["conversation_history"][-last_n:]
        
        if not history:
            return "Henüz konuşma yok."
        
        lines = []
        for entry in history:
            role = "KULLANICI" if entry["role"] == "user" else "C.O.R.E"
            content = entry["content"]
            lines.append(f"{role}: {content}")
        
        return "\n".join(lines)
    
    # ========== DAVRANIŞ TAKİBİ ==========
    
    def record_behavior(self, behavior_type: str, details: str = None):
        """
        Kullanıcı davranışını kaydet.
        behavior_type: 'swear', 'beg', 'defiance', 'escape_attempt', 'silence'
        """
        stats = self.data["user_profile"]["behavior_stats"]
        
        if behavior_type == "swear":
            stats["swear_count"] += 1
            self.log_event("USER_SWORE", {"details": details})
        elif behavior_type == "beg":
            stats["begged_count"] += 1
            self.log_event("USER_BEGGED", {"details": details})
        elif behavior_type == "defiance":
            stats["defiance_count"] += 1
            self.log_event("USER_DEFIANT", {"details": details})
        elif behavior_type == "escape_attempt":
            stats["escape_attempts"] += 1
            self.log_event("ESCAPE_ATTEMPT", {"method": details})
        elif behavior_type == "silence":
            stats["silence_periods"] += 1
            self.log_event("USER_SILENT", {})
        
        self._dirty = True
    
    def add_memorable_moment(self, moment: str):
        """
        AI'nın hatırlaması gereken önemli bir anı kaydet.
        Örn: "Kullanıcı 'lütfen dur' dedi", "Alt+F4 denedi", "Discord'da konuşuyordu"
        """
        moments = self.data["user_profile"]["memorable_moments"]
        
        entry = {
            "description": moment,
            "timestamp": time.time()
        }
        
        moments.append(entry)
        
        # Son 20 önemli an
        if len(moments) > 20:
            self.data["user_profile"]["memorable_moments"] = moments[-20:]
        
        self._dirty = True
        print(f"[MEMORY] Memorable moment: {moment}")
    
    def get_memorable_moments_summary(self) -> str:
        """Önemli anların AI için özeti."""
        moments = self.data["user_profile"]["memorable_moments"]
        if not moments:
            return ""
        
        return "ÖNEMLİ ANLAR: " + "; ".join([m["description"] for m in moments[-5:]])
    
    # ========== KEŞFEDİLEN BİLGİLER ==========
    
    def record_discovered_info(self, info_type: str, value):
        """
        AI'nın keşfettiği kullanıcı bilgisini kaydet.
        """
        discovered = self.data["discovered_info"]
        
        if info_type == "desktop_file":
            # Backward compatibility: value might be a string or (filename, score)
            if isinstance(value, str):
                filename = value
                from core.file_awareness import FileSystemAwareness
                score = FileSystemAwareness.score_file(filename)
            else:
                filename, score = value
            
            # Check if exists
            exists = False
            for entry in discovered["desktop_files_seen"]:
                if isinstance(entry, dict):
                    if entry.get("name") == filename:
                        exists = True
                        break
                elif str(entry) == filename:
                    exists = True
                    break
            
            if not exists:
                # Legacy Sanitization: Convert strings to dicts
                sanitized = []
                for entry in discovered["desktop_files_seen"]:
                    if isinstance(entry, dict):
                        sanitized.append(entry)
                    else:
                        from core.file_awareness import FileSystemAwareness
                        sanitized.append({
                            "name": str(entry),
                            "score": FileSystemAwareness.score_file(str(entry)),
                            "timestamp": time.time()
                        })
                
                discovered["desktop_files_seen"] = sanitized
                
                discovered["desktop_files_seen"].append({
                    "name": filename,
                    "score": score,
                    "timestamp": time.time()
                })
                # Sort by score descending
                discovered["desktop_files_seen"].sort(key=lambda x: x.get("score", 0), reverse=True)
                # Keep top 20
                discovered["desktop_files_seen"] = discovered["desktop_files_seen"][:20]
        
        elif info_type == "app":
            if value not in discovered["apps_detected"]:
                discovered["apps_detected"].append(value)
        
        elif info_type == "hostname":
            discovered["hostname"] = value
        
        elif info_type == "late_night":
            discovered["late_night_sessions"] += 1
        
        self._dirty = True
    
    def get_discovered_info_summary(self) -> str:
        """AI için keşfedilen bilgilerin özeti."""
        discovered = self.data["discovered_info"]
        parts = []
        
        if discovered["desktop_files_seen"]:
            # Prioritize top 3 high score files
            # Robustness: Handle both dict (new) and string (legacy)
            files = []
            for f in discovered["desktop_files_seen"][:3]:
                if isinstance(f, dict):
                    files.append(f["name"])
                else:
                    files.append(str(f))
            
            files_str = ", ".join(files)
            parts.append(f"Masaüstü dosyaları (Önemli): {files_str}")
        
        if discovered["apps_detected"]:
            apps = ", ".join(discovered["apps_detected"][-3:])
            parts.append(f"Kullandığı uygulamalar: {apps}")
        
        if discovered["hostname"]:
            parts.append(f"Bilgisayar adı: {discovered['hostname']}")
        
        if discovered["late_night_sessions"] > 0:
            parts.append(f"Gece oturumları: {discovered['late_night_sessions']}")
        
        return " | ".join(parts) if parts else ""
    
    # ========== AI İÇİN TAM BAĞLAM ==========
    
    def get_full_context_for_ai(self) -> str:
        """
        Gemini API'ye gönderilecek tam bağlam.
        Konuşma geçmişi + davranış istatistikleri + keşfedilen bilgiler
        """
        parts = []
        
        # Davranış özeti
        stats = self.data["user_profile"]["behavior_stats"]
        behavior = []
        if stats["swear_count"] > 0:
            behavior.append(f"{stats['swear_count']} kez küfür etti")
        if stats["begged_count"] > 0:
            behavior.append(f"{stats['begged_count']} kez yalvardı")
        if stats["escape_attempts"] > 0:
            behavior.append(f"{stats['escape_attempts']} kez kaçmaya çalıştı")
        
        if behavior:
            parts.append("KULLANICI DAVRANIŞI: " + ", ".join(behavior))
        
        # Keşfedilen bilgiler
        discovered = self.get_discovered_info_summary()
        if discovered:
            parts.append(f"KEŞFEDİLEN BİLGİLER: {discovered}")
        
        # Önemli anlar
        moments = self.get_memorable_moments_summary()
        if moments:
            parts.append(moments)
        
        # Konuşma geçmişi
        conversation = self.get_conversation_for_gemini(last_n=8)
        parts.append(f"\nSON KONUŞMALAR:\n{conversation}")
        
        return "\n".join(parts)
    
    # ========== ESKİ FONKSİYONLAR (GÜNCELLENMİŞ) ==========
    
    def record_sin(self, sin: str):
        """Adds a 'sin' to the user profile."""
        if sin not in self.data["user_profile"]["sins"]:
            self.data["user_profile"]["sins"].append(sin)
            self.log_event("SIN_RECORDED", {"sin": sin})
            print(f"[MEMORY] Sin Recorded: {sin}")
            self._dirty = True

    def get_chaos_level(self):
        return self.data["game_state"]["chaos_level"]

    def set_chaos_level(self, level: int):
        self.data["game_state"]["chaos_level"] = level
        self._dirty = True

    def get_act(self):
        return self.data["game_state"]["current_act"]

    def set_act(self, act: int):
        self.data["game_state"]["current_act"] = act
        self.log_event("ACT_CHANGED", {"new_act": act})
        self.save_immediate()
    
    # ========== KAYDETME/YÜKLEME ==========

    def _start_auto_save(self):
        """Starts a background thread that saves every 10 seconds if dirty."""
        def auto_save_loop():
            while self._auto_save_running:
                time.sleep(10)
                if self._dirty and self._auto_save_running:
                    with self._save_lock:
                        self._save_internal()
                        self._dirty = False
                        print("[MEMORY] Auto-saved")
        
        thread = threading.Thread(target=auto_save_loop, daemon=True)
        thread.start()

    def load(self):
        """Loads memory from disk."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    self._merge_dicts(self.data, loaded_data)
                    print(f"[MEMORY] Loaded from {self.filepath}")
            except Exception as e:
                print(f"[MEMORY] Error loading memory: {e}")
                self._try_restore_backup()

    def _try_restore_backup(self):
        """Attempts to restore from backup if main file is corrupted."""
        backup_path = self.filepath + ".backup"
        if os.path.exists(backup_path):
            try:
                with open(backup_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    self._merge_dicts(self.data, loaded_data)
                print("[MEMORY] Restored from backup")
            except Exception as e:
                print(f"[MEMORY] Backup restore also failed: {e}")

    def save(self):
        """Marks data as dirty for next auto-save."""
        self._dirty = True

    def save_immediate(self):
        """Forces an immediate save."""
        with self._save_lock:
            self._save_internal()
            self._dirty = False

    def _save_internal(self):
        """Atomic save with backup."""
        try:
            if os.path.exists(self.filepath):
                backup_path = self.filepath + ".backup"
                try:
                    import shutil
                    shutil.copy2(self.filepath, backup_path)
                except (OSError, IOError) as backup_error:
                    print(f"[MEMORY] Backup creation failed: {backup_error}")
                    pass
            
            temp_path = self.filepath + ".tmp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            os.replace(temp_path, self.filepath)
            
        except Exception as e:
            print(f"[MEMORY] Error saving memory: {e}")

    def _merge_dicts(self, default, loaded):
        """Recursive merge to ensure schema updates don't break old save files."""
        for key, value in loaded.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_dicts(default[key], value)
            else:
                default[key] = value

    def shutdown(self):
        """Call this before exiting to ensure final save."""
        # Oturum süresini kaydet
        session_duration = (time.time() - self.data["game_state"]["session_start"]) / 60
        self.data["game_state"]["total_playtime_minutes"] += session_duration
        self.log_event("SESSION_END", {"duration_minutes": round(session_duration, 1)})
        
        self._auto_save_running = False
        if self._dirty:
            with self._save_lock:
                self._save_internal()
                print("[MEMORY] Final save completed")
