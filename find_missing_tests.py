#!/usr/bin/env python3
"""Check which tests were NOT run"""
import subprocess
import sys

# Get all test IDs that pytest would collect
result = subprocess.run(
    [sys.executable, "-m", "pytest", "--collect-only", "-q"],
    capture_output=True,
    text=True,
    cwd=r"C:\Users\Betül Büyük\Downloads\megasentito\v8\SENTIENT_OS"
)

all_tests = []
for line in result.stdout.split('\n'):
    line = line.strip()
    if '::' in line and not line.startswith('=') and not line.startswith('<'):
        # Extract test ID
        all_tests.append(line)

print(f"Total tests collected by pytest: {len(all_tests)}")

# Now read which ones were actually run
with open(r'C:\Users\Betül Büyük\Downloads\megasentito\v8\SENTIENT_OS\tests\debug_trace.log', 'r', encoding='utf-8') as f:
    run_tests = []
    for line in f:
        if 'SETUP:' in line:
            test_id = line.split('SETUP:')[1].strip()
            run_tests.append(test_id)

print(f"Tests actually run (SETUP): {len(run_tests)}")
print(f"Tests NOT run: {len(all_tests) - len(run_tests)}")

# Find missing tests
run_tests_set = set(run_tests)
all_tests_set = set(all_tests)
missing = all_tests_set - run_tests_set

if missing:
    print("\n❌ Tests that were NEVER started:")
    for test in sorted(missing):
        print(f"  {test}")
