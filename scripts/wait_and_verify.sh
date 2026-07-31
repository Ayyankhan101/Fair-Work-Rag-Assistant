#!/bin/bash
# DEF-022: Verification script that propagates failures
# Usage: ./scripts/wait_and_verify.sh [timeout_seconds] [check_interval]

set -euo pipefail

TIMEOUT="${1:-60}"
CHECK_INTERVAL="${2:-5}"
ELAPSED=0

echo "Waiting for service to be ready (timeout: ${TIMEOUT}s)..."

while [ $ELAPSED -lt $TIMEOUT ]; do
    # Check if app is responding on port 7860
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:7860 2>/dev/null | grep -q "200\|302"; then
        echo "Service is ready after ${ELAPSED}s"
        exit 0
    fi
    
    sleep $CHECK_INTERVAL
    ELAPSED=$((ELAPSED + CHECK_INTERVAL))
    echo "  Still waiting... (${ELAPSED}/${TIMEOUT}s)"
done

echo "ERROR: Service did not become ready within ${TIMEOUT}s"
exit 1
