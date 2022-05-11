set PYTHONPATH=../;
start "GatewaySrv" cmd /c "python -m service.gateway.GatewaySrv 50100 & pause"
pause