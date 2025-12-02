#!/usr/bin/env bash
set -euo pipefail

# Base dir with server.py
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Configurable port (default 8000)
PORT="${PORT:-8000}"

# Stop by pidfile if present
PID_FILE="$BASE_DIR/server.pid"
if [[ -f "$PID_FILE" ]]; then
  PID="$(cat "$PID_FILE" || true)"
  if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
    echo "Stopping server (pid $PID)..."
    kill "$PID" || true
    # give it a moment to shutdown
    for i in {1..10}; do
      if kill -0 "$PID" 2>/dev/null; then
        sleep 0.2
      else
        break
      fi
    done
  fi
  rm -f "$PID_FILE"
fi

# Kill any stray server.py processes as fallback
if pgrep -f "server.py" >/dev/null 2>&1; then
  echo "Killing stray server.py processes..."
  pkill -f "server.py" || true
  sleep 0.2
fi

# Start server in background, redirect logs, write pidfile
echo "Starting server on port $PORT..."
nohup python3 server.py > server.log 2>&1 &
NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"
echo "Server started with pid $NEW_PID. Logs: $BASE_DIR/server.log"

# Open browser if $BROWSER is available
if [[ -n "${BROWSER:-}" ]] && command -v "$BROWSER" >/dev/null 2>&1; then
  "$BROWSER" "http://localhost:$PORT" >/dev/null 2>&1 || true
else
  echo "Open your browser at http://localhost:$PORT"
fi
