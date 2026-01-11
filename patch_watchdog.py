import re

filepath = r"c:\Users\Betül Büyük\Downloads\megasentito\v8\SENTIENT_OS\story\story_manager.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if already has the cancel call
if '_cancel_transition_watchdog()' not in content:
    # Find and replace the method
    pattern = r'(    def _actually_load_next_act\(self, act_num: int\):\n        """Actually loads the next act after transition."""\n)'
    replacement = r'\1        self._cancel_transition_watchdog()\n'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Added watchdog cancel call")
    else:
        print("⚠️ Pattern not found")
else:
    print("✅ Watchdog cancel already present")
