@echo off
REM Przechodzenie do katalogu, w którym znajduje się plik .bat
cd /d "%~dp0"

REM Aktywacja środowiska wirtualnego
echo Activating virtual environment...
call "..\.venv\Scripts\activate.bat"

REM Uruchomienie Redis na WSL
echo Starting Redis on WSL...
wsl redis-server --daemonize yes

REM Uruchomienie Daphne
echo Starting Daphne...
daphne -b 127.0.0.1 -p 8000 dzielimysie_tu.asgi:application

REM Zatrzymanie Redis po zamknięciu Daphne
echo Stopping Redis on WSL...
wsl redis-cli shutdown

REM Czekanie na potwierdzenie od użytkownika przed zamknięciem
pause