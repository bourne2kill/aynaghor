#!/bin/bash
# One‑click script that stops containers, backs up workspace/, and restarts.

echo "🔄 AYNAGH0R Recovery Script"
echo "=========================="

# Stop running services
echo "Stopping services..."
pkill -f "streamlit run"
pkill -f "uvicorn agent.main:app"

# Create backup
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "Creating backup in $BACKUP_DIR..."
cp -r workspace/ "$BACKUP_DIR/"
cp -r KH4NK1/ "$BACKUP_DIR/"
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR/"
rm -rf "$BACKUP_DIR"
echo "Backup created: $BACKUP_DIR.tar.gz"

# Restart services
echo "Restarting services..."
cd workspace/aynaghor
streamlit run ui/app.py --server.port 12000 --server.address 0.0.0.0 --server.enableCORS false > /tmp/streamlit.log 2>&1 &
cd ../../KH4NK1
uvicorn agent.main:app --host 0.0.0.0 --port 12001 > /tmp/fastapi.log 2>&1 &

sleep 3
echo "Services restarted!"
echo "UI: https://work-1-xdvectxuifefgzls.prod-runtime.all-hands.dev"
echo "API: https://work-2-xdvectxuifefgzls.prod-runtime.all-hands.dev"