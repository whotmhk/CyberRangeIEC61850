@echo off
:: Check for administrative permissions
net session >nul 2>&1
if %errorLevel% == 0 (
    :: We are running with administrative permissions
    if "%~x1" == ".py" (
        python %*
    ) else (
        %*
    )
) else (
    :: We are not running with administrative permissions, request elevation
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\elevate.vbs"
    echo UAC.ShellExecute "cmd.exe", "/c ""%~f0"" %*", "", "runas", 1 >> "%temp%\elevate.vbs"
    "%temp%\elevate.vbs"
    del "%temp%\elevate.vbs"
)
exit /b
