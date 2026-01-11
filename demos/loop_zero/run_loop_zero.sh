#!/bin/bash
#
# Loop Zero Runner - Start all processes for concurrent proof-of-concept
#
# Usage:
#   ./run_loop_zero.sh          # Start all processes
#   ./run_loop_zero.sh stop     # Stop all processes
#   ./run_loop_zero.sh status   # Show running processes
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Configuration
export MQTT_HOST="${MQTT_HOST:-localhost}"
export MQTT_PORT="${MQTT_PORT:-1883}"
export SCOPE="${SCOPE:-demo_room}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_mosquitto() {
    if ! command -v mosquitto &> /dev/null; then
        log_error "Mosquitto not found. Install with: sudo apt install mosquitto"
        exit 1
    fi

    if ! pgrep -x mosquitto > /dev/null; then
        log_error "Mosquitto broker not running. Start with: mosquitto -d"
        exit 1
    fi

    log_info "Mosquitto broker running"
}

check_paho() {
    if ! python3 -c "import paho.mqtt.client" 2>/dev/null; then
        log_error "paho-mqtt not installed. Install with: pip install paho-mqtt"
        exit 1
    fi
}

start_processes() {
    log_info "Starting Loop Zero processes..."
    log_info "MQTT: $MQTT_HOST:$MQTT_PORT"
    log_info "Scope: $SCOPE"
    echo ""

    # Start each process in background
    python3 loop_zero_cortex.py &
    CORTEX_PID=$!
    log_info "Cortex started (PID: $CORTEX_PID)"

    python3 loop_zero_thalamus.py &
    THALAMUS_PID=$!
    log_info "Thalamus started (PID: $THALAMUS_PID)"

    python3 loop_zero_trn.py &
    TRN_PID=$!
    log_info "TRN started (PID: $TRN_PID)"

    echo ""
    log_info "All processes started!"
    echo ""
    echo "Process PIDs:"
    echo "  Cortex:   $CORTEX_PID"
    echo "  Thalamus: $THALAMUS_PID"
    echo "  TRN:      $TRN_PID"
    echo ""
    echo "To stop: ./run_loop_zero.sh stop"
    echo "To view logs: tail -f the terminal outputs"
    echo ""
    echo "Press Ctrl+C to stop all processes..."

    # Wait for all processes
    wait
}

stop_processes() {
    log_info "Stopping Loop Zero processes..."

    # Find and kill processes
    pkill -f "loop_zero_cortex.py" 2>/dev/null && log_info "Stopped Cortex" || true
    pkill -f "loop_zero_thalamus.py" 2>/dev/null && log_info "Stopped Thalamus" || true
    pkill -f "loop_zero_trn.py" 2>/dev/null && log_info "Stopped TRN" || true

    log_info "All processes stopped"
}

show_status() {
    echo "Loop Zero Process Status:"
    echo ""

    ps aux | grep -E "loop_zero_(cortex|thalamus|trn)" | grep -v grep || echo "No Loop Zero processes running"

    echo ""
    echo "Mosquitto status:"
    if pgrep -x mosquitto > /dev/null; then
        echo "  Running (PID: $(pgrep -x mosquitto))"
    else
        echo "  Not running"
    fi
}

# Main
case "${1:-start}" in
    start)
        check_mosquitto
        check_paho
        start_processes
        ;;
    stop)
        stop_processes
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
        ;;
esac
