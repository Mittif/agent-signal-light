#!/bin/bash
# Forward an agent hook's stdin JSON to the local light daemon.
# Always exit 0 so we never inadvertently block the parent agent.
# Bound timeout so a missing/hung daemon adds at most 1s of latency.
curl -fsS --max-time 1 \
     -X POST http://127.0.0.1:7878/hook \
     -H "Content-Type: application/json" \
     --data-binary @- \
     >/dev/null 2>&1
exit 0
