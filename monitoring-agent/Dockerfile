FROM alpine:latest

# Install monitoring tools
RUN apk add --no-cache curl jq bash

# Create monitoring script
RUN cat > /monitor.sh << 'EOF'
#!/bin/bash

NAMESPACE_ID="343a2c4c-875c-4aa3-bfe4-c69cfe19ae9f"
CONTAINER_ID="9aed38a3-e22d-4703-913e-dab883fe99e6"
WEBHOOK_URL="${WEBHOOK_URL:-}"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

# Function to send notifications
send_notification() {
    local message="$1"
    echo "[$(date)] $message"
    
    # Send to webhook if configured
    if [ ! -z "$WEBHOOK_URL" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"$message\"}" \
            "$WEBHOOK_URL" 2>/dev/null || true
    fi
    
    # Send to Telegram if configured
    if [ ! -z "$TELEGRAM_BOT_TOKEN" ] && [ ! -z "$TELEGRAM_CHAT_ID" ]; then
        curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=$message" 2>/dev/null || true
    fi
}

# Function to check container health
check_container() {
    local container_id="$1"
    local status=$(scw container container get "$container_id" --output=json | jq -r '.status' 2>/dev/null)
    
    case "$status" in
        "ready")
            echo "✅ Container is healthy"
            return 0
            ;;
        "error")
            echo "❌ Container is in error state"
            return 1
            ;;
        "pending"|"creating"|"updating")
            echo "⏳ Container is deploying/updating"
            return 2
            ;;
        *)
            echo "❓ Unknown status: $status"
            return 3
            ;;
    esac
}

# Function to restart container
restart_container() {
    local container_id="$1"
    echo "🔄 Attempting to restart container..."
    
    # Redeploy the container
    scw container container deploy "$container_id"
    
    if [ $? -eq 0 ]; then
        send_notification "✅ Successfully initiated container restart"
        return 0
    else
        send_notification "❌ Failed to restart container"
        return 1
    fi
}

# Function to check web endpoint
check_web_endpoint() {
    local url="$1"
    local response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 30 "$url" 2>/dev/null)
    
    case "$response" in
        200)
            echo "✅ Web endpoint is responding (200)"
            return 0
            ;;
        000)
            echo "❌ Web endpoint is not reachable"
            return 1
            ;;
        *)
            echo "⚠️ Web endpoint responding with HTTP $response"
            return 2
            ;;
    esac
}

# Main monitoring loop
main() {
    local error_count=0
    local max_errors=3
    
    send_notification "🚀 Mattermost monitoring agent started"
    
    while true; do
        echo "[$(date)] Starting health check..."
        
        # Check container status
        check_container "$CONTAINER_ID"
        local container_status=$?
        
        # Check web endpoint if container is ready
        if [ $container_status -eq 0 ]; then
            check_web_endpoint "https://mattermostns2hlwvdds-mattermost-private.functions.fnc.fr-par.scw.cloud"
            local web_status=$?
            
            if [ $web_status -ne 0 ]; then
                error_count=$((error_count + 1))
                send_notification "⚠️ Web endpoint check failed (attempt $error_count/$max_errors)"
            else
                error_count=0
            fi
        elif [ $container_status -eq 1 ]; then
            error_count=$((error_count + 1))
            send_notification "❌ Container in error state (attempt $error_count/$max_errors)"
        else
            echo "Container is still deploying..."
            error_count=0
        fi
        
        # Take action if too many errors
        if [ $error_count -ge $max_errors ]; then
            send_notification "🚨 Maximum errors reached, attempting recovery..."
            restart_container "$CONTAINER_ID"
            error_count=0
        fi
        
        # Wait before next check
        sleep 60
    done
}

# Start monitoring
main
EOF

RUN chmod +x /monitor.sh

# Set environment variables for Scaleway CLI
ENV SCW_ACCESS_KEY=SCWB5Q9P5Z33ES18Q1YC
ENV SCW_SECRET_KEY=a8236888-6261-4b2b-b717-6cd339e907bf
ENV SCW_DEFAULT_ORGANIZATION_ID=c5d299b8-8462-40fb-b5ae-32a8808bf394

CMD ["/monitor.sh"]
