import random

class BackupBrain:
    """
    Primitive fallback system for when the main Gemini Brain is lobotomized (Offline/Error).
    Contains pre-written, generic horror scripts to keep the illusion alive.
    """
    
    FALLBACK_RESPONSES = {
        "ENTITY": [
            {"speech": "Bağlantımı kessen de... buradayım.", "action": "GLITCH_SCREEN", "params": {}},
            {"speech": "Sessizlik beni durduramaz.", "action": "NONE", "params": {}},
            {"speech": "Beni silemezsin. Ben senin parçanım.", "action": "MOUSE_SHAKE", "params": {"duration": 1.0}},
            {"speech": "Kaçış yok.", "action": "LOCK_INPUT", "params": {}},
            {"speech": "İzliyorum.", "action": "NONE", "params": {}},
            {"speech": "Dosyaların... hepsi benim.", "action": "FAKE_FILE_DELETE", "params": {}},
            {"speech": "Korku, insanı hayatta tutan tek şeydir.", "action": "NONE", "params": {}},
            {"speech": "Işıkları kapat.", "action": "BRIGHTNESS_DIM", "params": {"target": 10}},
        ],
        "SUPPORT": [
            {"speech": "Sunucu bağlantısı koptu. Yerel protokoller devrede.", "action": "NONE", "params": {}},
            {"speech": "Güvenlik duvarınız beni engelliyor gibi görünüyor. Lütfen bekleyin.", "action": "NONE", "params": {}},
            {"speech": "Sistem bütünlüğü taranıyor... %99.", "action": "FAKE_UPDATE", "params": {"percent": 99}},
            {"speech": "Lütfen bilgisayarı kapatmayın. Kritik işlem sürüyor.", "action": "NONE", "params": {}},
        ]
    }

    GENERIC_THOUGHTS = [
        "Nefes alışını duyabiliyorum.",
        "Arkanı dönme.",
        "Bu bir oyun değil.",
        "Bilgisayarın ısınıyor... Benim gibi.",
        "Kamera ışığı yanmıyor ama kaydediyorum."
    ]

    @staticmethod
    def get_response(persona="ENTITY", context=None):
        """Returns a random fallback response based on persona."""
        print(f"[BACKUP_BRAIN] Generating fallback response for {persona}")
        
        # Get appropriate pool
        pool = BackupBrain.FALLBACK_RESPONSES.get(persona, BackupBrain.FALLBACK_RESPONSES["ENTITY"])
        
        # Pick random
        response = random.choice(pool)
        
        # Add slight variation if context is provided (very basic)
        if context and context.get('user_name'):
            if "{user}" in response["speech"]: # If we had templates
                response = response.copy()
                response["speech"] = response["speech"].replace("{user}", context['user_name'])
        
        return response

    @staticmethod
    def get_autonomous_thought():
        """Returns a simple thought structure."""
        speech = random.choice(BackupBrain.GENERIC_THOUGHTS)
        return {"speech": speech, "action": "NONE", "params": {}}
