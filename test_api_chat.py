
import asyncio
import sys
import os

# Add SDK path to sys.path
sys.path.append(os.path.join(os.getcwd(), 'sdk'))

from sentientos.client import SentientClient
from core.config_manager import ConfigManager

async def main():
    config = ConfigManager()
    
    url = config.get('server.edge_url', 'http://localhost:8000')
    token = config.get('server.jwt_token', '')
    device_id = config.get('server.device_id', 'test_device')
    
    print("\n" + "="*50)
    print(" 🤖 SENTIENT_OS SERVER TEST CHAT")
    print(f" Connecting to: {url}")
    print(f" Device ID: {device_id}")
    print("="*50 + "\n")
    
    if not token:
        print("❌ ERROR: No JWT_TOKEN found in config.yaml!")
        return

    async with SentientClient(base_url=url, token=token, device_id=device_id) as client:
        # Check health first
        try:
            health = await client.get_health()
            print(f"✅ Server Health: {health.get('status', 'unknown')}")
        except Exception as e:
            print(f"❌ Server Connection Failed: {e}")
            return

        print("\n(Type 'exit' to quit)\n")
        
        while True:
            user_input = input("👤 You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            print("⏳ Thinking...", end="\r")
            
            try:
                # Add some context dummy data
                context = {
                    "persona": "ENTITY",
                    "user_name": "TestUser",
                    "anger_level": 50,
                    "current_act": 1
                }
                
                response = await client.infer(user_input, context)
                
                print(f"\r🤖 AI: {response.text}")
                if response.actions:
                    print(f"🎬 Actions: {response.actions}")
                print("-" * 30)
                
            except Exception as e:
                print(f"\r❌ Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
