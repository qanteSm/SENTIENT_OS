#!/usr/bin/env python3
"""Quick script to analyze debug_trace.log"""

with open(r'tests\debug_trace.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

setup_tests = []
teardown_tests = []

for line in lines:
    if 'SETUP:' in line:
        test_name = line.split('SETUP:')[1].strip()
        setup_tests.append(test_name)
    elif 'TEARDOWN:' in line:
        test_name = line.split('TEARDOWN:')[1].strip()
        teardown_tests.append(test_name)

print(f"Total SETUP: {len(setup_tests)}")
print(f"Total TEARDOWN: {len(teardown_tests)}")
print(f"Missing TEARDOWN: {len(setup_tests) - len(teardown_tests)}")

# Find which tests are missing teardown
missing = set(setup_tests) - set(teardown_tests)
if missing:
    print("\n❌ Tests missing TEARDOWN:")
    for test in missing:
        print(f"  - {test}")

# Check if SESSION FINISH was logged
session_finish = any('SESSION FINISH' in line for line in lines)
print(f"\n✅ SESSION FINISH logged: {session_finish}")

# Show last 5 lines
print("\n📄 Last 5 lines of trace:")
for line in lines[-5:]:
    print(f"  {line.rstrip()}")
