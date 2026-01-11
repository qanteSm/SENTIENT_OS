@echo off
echo ===================================================
echo   SENTIENT_OS FINAL VERIFICATION & STRESS TEST
echo ===================================================
echo.
echo Running Unit Tests...
python -m pytest tests/unit -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Unit Tests Failed!
) else (
    echo [SUCCESS] Unit Tests Passed!
)
echo.
echo Running Integration Tests...
python -m pytest tests/integration -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Integration Tests Failed!
) else (
    echo [SUCCESS] Integration Tests Passed!
)
echo.
echo Running Stress Tests (Full Suite)...
python -m pytest tests/stress/test_memory_stress.py -v -m stress
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Memory Stress Failed!
) else (
    echo [SUCCESS] Memory Stress Passed!
)
echo.
echo Running Dispatcher Stress...
python -m pytest tests/stress/test_dispatcher_stress.py -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Dispatcher Stress Failed!
) else (
    echo [SUCCESS] Dispatcher Stress Passed!
)
echo.
echo Running Chaos Monkey...
python -m pytest tests/stress/test_chaos_monkey.py -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Chaos Monkey Failed!
) else (
    echo [SUCCESS] Chaos Monkey Passed!
)
echo.
echo ===================================================
echo   ALL TESTS COMPLETED - CHECK OUTPUT ABOVE
echo ===================================================
pause
