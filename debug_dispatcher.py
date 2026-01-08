
from core.function_dispatcher import FunctionDispatcher

def test_dispatcher():
    dispatcher = FunctionDispatcher()
    
    # CASE 1: Normal
    print("Testing Normal...")
    dispatcher.dispatch({"action": "NONE", "params": {}})
    
    # CASE 2: Params is None (JSON: "params": null)
    print("Testing Null Params...")
    try:
        dispatcher.dispatch({"action": "NONE", "params": None})
        print("SUCCESS: Handled None params")
    except Exception as e:
        print(f"FAIL: Crashed on None params: {e}")

    # CASE 3: Missing Params
    print("Testing Missing Params...")
    try:
        dispatcher.dispatch({"action": "NONE"})
        print("SUCCESS: Handled missing params")
    except Exception as e:
        print(f"FAIL: Crashed on missing params: {e}")

    # CASE 4: Missing Title in Notification
    print("Testing Missing Title...")
    try:
        dispatcher.dispatch({"action": "FAKE_NOTIFICATION", "params": {}})
        print("SUCCESS: Handled missing title")
    except Exception as e:
        print(f"FAIL: Crashed on missing title: {e}")

if __name__ == "__main__":
    test_dispatcher()
