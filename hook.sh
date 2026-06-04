#!/bin/bash
# Forward an agent hook's stdin JSON to the local light daemon.
# Always exit 0 so we never inadvertently block the parent agent.
# Bound timeout so a missing/hung daemon adds at most 1s of latency.
agent="${1:-unknown}"
case "$agent" in
  claude|codex) ;;
  *) agent="unknown" ;;
esac
log_dir="${HOME}/.agent-signal-light"
log_file="${log_dir}/hook.log"
mkdir -p "$log_dir" 2>/dev/null
printf '%s agent=%s dispatch\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$agent" >>"$log_file" 2>/dev/null
curl -fsS --max-time 1 \
     -X POST "http://127.0.0.1:7878/hook?agent=${agent}" \
     -H "Content-Type: application/json" \
     --data-binary @- \
     >/dev/null 2>&1
printf '%s agent=%s curl_rc=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$agent" "$?" >>"$log_file" 2>/dev/null
exit 0
