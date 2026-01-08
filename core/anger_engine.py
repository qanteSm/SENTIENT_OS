import random

class AngerEngine:
    """
    Calculates the AI's stress/anger level based on user interactions.
    Controls the frequency and intensity of chaos events.
    """
    def __init__(self):
        self.current_anger = 0 # 0 to 100
        # Penalties for specific actions
        self.penalties = {
            "swear": 15,
            "alt_f4": 25,
            "task_manager": 20,
            "mute_audio": 10,
            "ignore": 5
        }
        # Rewards (Reducing anger)
        self.rewards = {
            "obedience": 5,
            "compliment": 10
        }

    def calculate_anger(self, user_action_type: str) -> int:
        """
        Adjusts anger level based on inputs.
        user_action_type: key from penalties or rewards dict.
        """
        if user_action_type in self.penalties:
            increase = self.penalties[user_action_type]
            self.current_anger = min(100, self.current_anger + increase)
            print(f"[ANGER] Anger increased by {increase}. Current: {self.current_anger}")
        
        elif user_action_type in self.rewards:
            decrease = self.rewards[user_action_type]
            self.current_anger = max(0, self.current_anger - decrease)
            print(f"[ANGER] Anger decreased by {decrease}. Current: {self.current_anger}")
            
        return self.current_anger

    def get_chaos_multiplier(self) -> float:
        """
        Returns a multiplier for event frequency based on anger.
        0-20 anger: 1.0x (Normal)
        21-50 anger: 1.5x (Agitated)
        51-80 anger: 2.0x (Aggressive)
        81-100 anger: 3.0x (Uncontrollable)
        """
        if self.current_anger <= 20:
            return 1.0
        elif self.current_anger <= 50:
            return 1.5
        elif self.current_anger <= 80:
            return 2.0
        else:
            return 3.0

    def should_trigger_autonomous_event(self) -> bool:
        """
        Determines if a random event should trigger based on anger level.
        Higher anger = Higher probability.
        """
        base_chance = 10 # 10% base chance per tick
        chance = base_chance + (self.current_anger * 0.5) 
        # Max chance around 60% per tick at 100 anger
        
        roll = random.uniform(0, 100)
        return roll < chance
