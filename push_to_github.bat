@echo off
echo ========================================================
echo Pushing Indian Railways AI ETA Prototype to GitHub...
echo Repository: https://github.com/ayuvan/indian-railways-ai-eta
echo ========================================================
echo.
".venv\Scripts\git.cmd" push -u origin main
echo.
if %ERRORLEVEL% equ 0 (
    echo ========================================================
    echo SUCCESS! Code pushed to GitHub successfully.
    echo Next step: Go to https://dashboard.render.com to deploy!
    echo ========================================================
) else (
    echo ========================================================
    echo Note: If prompted, please click 'Sign in with your browser'
    echo to authorize GitHub to upload your code.
    echo ========================================================
)
echo.
pause
