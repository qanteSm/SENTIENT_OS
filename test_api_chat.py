# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================


import sys
import os

# Add core modules to path
sys.path.insert(0, os.getcwd())

from core.gemini_brain import GeminiBrain
from core.memory import Memory
from core.config_manager import ConfigManager

def main():
    config = ConfigManager()
    
    print("\n" + "="*50)
    print(" 🤖 SENTIENT_OS CHAT TEST")
    print(" Using GeminiBrain (Same as game)")
    print("="*50 + "\n")
    
    # Check if server mode is enabled or if we have API key
    server_enabled = config.get('server.enabled', False)
    api_key = config.get('api.gemini_key', '')
    
    if not server_enabled and not api_key:
        print("❌ ERROR: Neither server mode nor Gemini API key configured!")
        print("   Please configure one of the following in config.yaml:")
        print("   1. Server mode:")
        print("      server:")
        print("        enabled: true")
        print("   2. Gemini API:")
        print("      api:")
        print("        gemini_key: YOUR_KEY_HERE")
        return
    
    # Initialize Memory and Brain (same as game)
    memory = Memory()
    brain = GeminiBrain()
    brain.set_memory(memory)
    
    # Display mode info
    if server_enabled:
        edge_url = config.get('server.edge_url', 'N/A')
        print(f"✅ Server Mode: {edge_url}")
    else:
        print("✅ Direct Gemini API Mode")
    
    print(f"✅ Current Persona: {brain.current_persona}")
    print("\nCommands:")
    print("  - Type 'exit' to quit")
    print("  - Type 'persona ENTITY' or 'persona SUPPORT' to switch persona")
    print("  - Type 'history' to see conversation history")
    print("-" * 50 + "\n")
    
    # Game-like context
    context = {
        "persona": brain.current_persona,
        "user_name": config.get('user.name', 'TestUser'),
        "anger_level": 50,
        "current_act": 1,
        "game_started": True,
        "phase": "exploration"
    }
    
    while True:
        user_input = input("👤 You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['exit', 'quit']:
            print("\n👋 Exiting...\n")
            break
        
        # Handle special commands
        if user_input.lower().startswith('persona '):
            persona_name = user_input[8:].strip().upper()
            if persona_name in ['ENTITY', 'SUPPORT']:
                brain.switch_persona(persona_name)
                context["persona"] = persona_name
                print(f"✅ Switched to persona: {persona_name}\n")
            else:
                print("❌ Invalid persona. Use: ENTITY or SUPPORT\n")
            continue
        
        if user_input.lower() == 'history':
            print("\n" + "="*50)
            print("CONVERSATION HISTORY")
            print("="*50)
            history = memory.get_conversation_history(limit=10)
            if history:
                for msg in history:
                    role = "👤 User" if msg["role"] == "user" else "🤖 AI"
                    print(f"{role}: {msg['message'][:100]}...")
            else:
                print("No conversation history yet.")
            print("="*50 + "\n")
            continue
        
        print("⏳ Thinking...", end="\r")
        
        try:
            # Call the exact same method the game uses
            response = brain.generate_response(user_input, context)
            
            # Display response (format matches game's expectation)
            speech = response.get("speech", "...")
            action = response.get("action", "idle")
            
            print(f"\r🤖 AI: {speech}")
            
            # Show action if not idle (game shows this too)
            if action != "idle" and action != "none":
                print(f"   🎬 Action: {action}")
            
            # Show anger effect if present
            if "anger_effect" in response:
                anger_delta = response["anger_effect"]
                if anger_delta != 0:
                    new_anger = context["anger_level"] + anger_delta
                    context["anger_level"] = max(0, min(100, new_anger))
                    print(f"   😠 Anger: {context['anger_level']} ({anger_delta:+d})")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"\r❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...\n")
