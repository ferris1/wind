set PYTHONPATH=../;

start "GameSrv" cmd /c "python -m service.game.GameSrv 50200 False & pause"

start "GatewaySrv" cmd /c "python -m service.gateway.GatewaySrv 50100 False & pause"
pause