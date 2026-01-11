@echo off
setlocal
echo ===================================================
echo   SENTIENT_OS ADVANCED CERTIFICATION SUITE
echo ===================================================
echo.
echo [1/2] Running Certified Tests & Resource Profiling...
echo (Pytest + HTML Report + Coverage + CPU/RAM Tracking)
python run_certified_tests.py
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Some tests failed or profiling was interrupted.
) else (
    echo [SUCCESS] Certification Suite completed successfully!
)
echo.
echo [2/2] Opening Advanced Reports...
start tests/report.html
start tests/coverage_report/index.html
if exist tests/performance_profile.png start tests/performance_profile.png
echo.
echo ===================================================
echo   CERTIFICATION COMPLETE
echo   - Interactive Report: tests/report.html
echo   - Coverage: tests/coverage_report/index.html
echo   - Profiling Summary: tests/performance_summary.md
echo ===================================================
pause
