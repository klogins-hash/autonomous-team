#!/bin/bash

# Mattermost Serverless Container Monitoring Script
CONTAINER_ID="9aed38a3-e22d-4703-913e-dab883fe99e6"
NAMESPACE_ID="343a2c4c-875c-4aa3-bfe4-c69cfe19ae9f"
MATTERMOST_URL="https://mattermostns2hlwvdds-mattermost-private.functions.fnc.fr-par.scw.cloud"
LOG_FILE="/tmp/mattermost-monitor.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log with timestamp
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to check container status
check_container_status() {
    local status=$(scw container container get "$CONTAINER_ID" --output=json 2>/dev/null | jq -r '.status' 2>/dev/null)
    echo "$status"
}

# Function to check web endpoint
check_web_endpoint() {
    local response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 --max-time 30 "$MATTERMOST_URL" 2>/dev/null)
    echo "$response"
}

# Function to get container metrics
get_container_metrics() {
    local metrics=$(scw container container get "$CONTAINER_ID" --output=json 2>/dev/null | jq -r '
    {
        "status": .status,
        "memory_limit": .memory_limit,
        "cpu_limit": .cpu_limit,
        "min_scale": .min_scale,
        "max_scale": .max_scale,
        "domain_name": .domain_name,
        "error_message": .error_message // "None"
    }' 2>/dev/null)
    echo "$metrics"
}

# Function to display status dashboard
display_dashboard() {
    clear
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}           MATTERMOST SERVERLESS CONTAINER MONITOR          ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    
    # Container Status
    local status=$(check_container_status)
    case "$status" in
        "ready")
            echo -e "📦 Container Status: ${GREEN}READY${NC} ✅"
            ;;
        "pending"|"creating"|"updating")
            echo -e "📦 Container Status: ${YELLOW}DEPLOYING${NC} ⏳"
            ;;
        "error")
            echo -e "📦 Container Status: ${RED}ERROR${NC} ❌"
            ;;
        *)
            echo -e "📦 Container Status: ${RED}UNKNOWN${NC} ❓ ($status)"
            ;;
    esac
    
    # Web Endpoint Status
    local http_code=$(check_web_endpoint)
    case "$http_code" in
        200)
            echo -e "🌐 Web Endpoint: ${GREEN}ONLINE${NC} ✅ (HTTP $http_code)"
            ;;
        000)
            echo -e "🌐 Web Endpoint: ${RED}OFFLINE${NC} ❌"
            ;;
        *)
            echo -e "🌐 Web Endpoint: ${YELLOW}WARNING${NC} ⚠️ (HTTP $http_code)"
            ;;
    esac
    
    echo
    echo -e "${BLUE}📊 Container Details:${NC}"
    local metrics=$(get_container_metrics)
    echo "$metrics" | jq -r '
    to_entries[] | 
    "  \(.key | gsub("_"; " ") | ascii_upcase): \(.value)"
    ' 2>/dev/null || echo "  Error retrieving metrics"
    
    echo
    echo -e "${BLUE}🔗 URLs:${NC}"
    echo "  Mattermost: $MATTERMOST_URL"
    echo "  Scaleway Console: https://console.scaleway.com/containers/namespaces/$NAMESPACE_ID"
    
    echo
    echo -e "${BLUE}📈 Recent Logs:${NC}"
    tail -10 "$LOG_FILE" 2>/dev/null | grep -v "═══════════════════════════════════════════════════════════════" || echo "  No logs available yet"
    
    echo
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE} Press Ctrl+C to stop monitoring | Auto-refresh every 30s ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
}

# Function to check for critical issues and suggest actions
check_critical_issues() {
    local status=$(check_container_status)
    local http_code=$(check_web_endpoint)
    
    if [[ "$status" == "error" ]]; then
        log "${RED}🚨 CRITICAL: Container is in ERROR state${NC}"
        log "${YELLOW}💡 Suggestion: Check container logs in Scaleway Console${NC}"
        log "${YELLOW}💡 Suggestion: Consider redeploying the container${NC}"
        return 1
    fi
    
    if [[ "$http_code" == "000" && "$status" == "ready" ]]; then
        log "${RED}🚨 CRITICAL: Container is ready but web endpoint is unreachable${NC}"
        log "${YELLOW}💡 Suggestion: Check port configuration and health checks${NC}"
        log "${YELLOW}💡 Suggestion: Verify environment variables${NC}"
        return 1
    fi
    
    if [[ "$status" == "pending" ]]; then
        log "${YELLOW}⏳ Container is still deploying...${NC}"
        return 2
    fi
    
    if [[ "$http_code" == "200" ]]; then
        log "${GREEN}✅ All systems operational${NC}"
        return 0
    fi
    
    return 3
}

# Main monitoring loop
main() {
    log "${BLUE}🚀 Starting Mattermost monitoring agent${NC}"
    log "${BLUE}📦 Container ID: $CONTAINER_ID${NC}"
    log "${BLUE}🌐 Monitoring URL: $MATTERMOST_URL${NC}"
    
    while true; do
        display_dashboard
        
        # Check for issues
        check_critical_issues
        local issue_level=$?
        
        # Sleep based on issue level
        if [[ $issue_level -eq 1 ]]; then
            sleep 10  # Check more frequently for critical issues
        elif [[ $issue_level -eq 2 ]]; then
            sleep 20  # Check moderately during deployment
        else
            sleep 30  # Normal interval
        fi
    done
}

# Trap to handle exit
trap 'log "${YELLOW}🛑 Monitoring stopped by user${NC}"; exit 0' INT TERM

# Start monitoring
main
