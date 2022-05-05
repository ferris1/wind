set PYTHONPATH=../;

start "GameSrv" cmd /c "chcp 65001 & python -m service.game.GameSrv 50100 & pause"

pause