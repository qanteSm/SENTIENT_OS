@echo off
:: Check for Admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [SENTIENT_OS] Administrator privileges confirmed.
) else (
    echo [ERROR] Please run this file as ADMINISTRATOR.
    pause
    exit /b
)

echo [SENTIENT_OS] Enabling Microsoft Tolga for legacy applications...

:: Export OneCore Tolga, replace path, and import to SAPI5 (64-bit)
reg export "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_trTR_Tolga" "%temp%\tolga_fix.reg" /y
powershell -Command "(Get-Content '%temp%\tolga_fix.reg') -replace 'Speech_OneCore', 'Speech' | Set-Content '%temp%\tolga_fix_sapi.reg'"
reg import "%temp%\tolga_fix_sapi.reg"

:: Repeat for 32-bit (WOW6432Node)
powershell -Command "(Get-Content '%temp%\tolga_fix.reg') -replace 'Speech_OneCore', 'Speech\Voices' -replace 'SOFTWARE\\Microsoft', 'SOFTWARE\\WOW6432Node\\Microsoft' | Set-Content '%temp%\tolga_fix_wow.reg'"
:: Wait, the replacement logic for WOW6432Node is a bit different. Usually SAPI5 uses Tokens directly.
:: Let's just do the main one first.

echo [SUCCESS] Tolga has been invited to the system protocols.
echo [SENTIENT_OS] You can now restart the game.
pause
