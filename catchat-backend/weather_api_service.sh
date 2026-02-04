#!/bin/bash
# weather_api_service.sh - Script to start the Weather API service

# Define paths
BACKEND_DIR="/root/catchat-backend"
VENV_PATH="$BACKEND_DIR/venv"
LOG_FILE="$BACKEND_DIR/weather_service_startup.log"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Change to the backend directory
cd "$BACKEND_DIR" || {
    log "ERROR: Could not change to directory $BACKEND_DIR"
    exit 1
}

# Make sure the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    log "ERROR: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Activate virtual environment
log "Activating virtual environment"
source "$VENV_PATH/bin/activate" || {
    log "ERROR: Failed to activate virtual environment"
    exit 1
}

# Check for Python
if ! command -v python &> /dev/null; then
    log "ERROR: Python not found in virtual environment"
    exit 1
fi

# Check for required files
if [ ! -f "$BACKEND_DIR/weather_api.py" ]; then
    log "ERROR: weather_api.py not found in $BACKEND_DIR"
    exit 1
fi

# Check for environment variables
if [ ! -f "$BACKEND_DIR/.env" ]; then
    log "WARNING: .env file not found in $BACKEND_DIR"
fi

# Start the Weather API
log "Starting Weather API service"
python "$BACKEND_DIR/weather_api.py" >> "$BACKEND_DIR/weather_api_output.log" 2>&1
