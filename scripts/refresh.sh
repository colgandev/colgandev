#!/bin/bash

reload_port() {
    local port=$1
    curl -s "http://localhost:$port/json" | \
    jq -r '.[] | select(.url | test("localhost|127.0.0.1")) | .webSocketDebuggerUrl' | \
    while read ws_url; do
        echo '{"id":1,"method":"Page.reload","params":{}}' | websocat -n1 "$ws_url" > /dev/null
    done
}

# Run each port in parallel
reload_port 9222
#reload_port 9223 &
#reload_port 9224 &

# Wait for all background jobs to complete
#wait
