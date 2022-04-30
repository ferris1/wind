set PYTHONPATH=../server;

start "GameSrv" cmd /c "chcp 65001 & python -m game.GameSrv 60300 & pause"

pause