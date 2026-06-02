@echo off
REM Forward an agent hook's stdin JSON to the local light daemon.
REM Always exit 0 so we never block the parent agent. 1-second cap so a
REM missing/hung daemon adds at most 1s of latency per hook firing.
curl -fsS --max-time 1 -X POST http://127.0.0.1:7878/hook ^
     -H "Content-Type: application/json" ^
     --data-binary @- >nul 2>&1
exit /b 0
