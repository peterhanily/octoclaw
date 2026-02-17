#!/bin/bash
# OpenClaw OctoClaw Skill Installation Script

set -e

echo "🦞 Installing OctoClaw skill for OpenClaw..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ Error: pip is required but not found"
    echo "Please install pip and try again"
    exit 1
fi

# Install required Python packages
echo "📦 Installing Python dependencies..."
python3 -m pip install --user requests || {
    echo "⚠️  Warning: Could not install requests. You may need to install it manually:"
    echo "  python3 -m pip install requests"
}

# Create config.json if it doesn't exist
if [ ! -f "$SKILL_DIR/config.json" ]; then
    echo "📝 Creating config.json from example..."
    cp "$SKILL_DIR/config.example.json" "$SKILL_DIR/config.json"
    echo ""
    echo "⚠️  IMPORTANT: Edit $SKILL_DIR/config.json with your settings:"
    echo "  - octoprint_url: Your Octoprint server address"
    echo "  - api_key: Your Octoprint API key"
    echo "  - webcam_url: Your webcam snapshot URL (optional)"
    echo "  - telegram_bot_token: Your Telegram bot token (optional)"
    echo "  - telegram_chat_id: Your Telegram chat ID (optional)"
    echo ""
else
    echo "✅ config.json already exists"
fi

# Make the Python script executable
chmod +x "$SKILL_DIR/scripts/octoprint.py" 2>/dev/null || true

echo ""
echo "✅ OctoClaw skill installed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit $SKILL_DIR/config.json with your Octoprint settings"
echo "2. Get your Octoprint API key from Settings > API in Octoprint web interface"
echo "3. (Optional) Set up Telegram bot for notifications"
echo "4. Use /octoclaw in OpenClaw to control your 3D printer"
echo ""
echo "Example commands:"
echo "  /octoclaw status    - Check printer status"
echo "  /octoclaw snapshot  - Capture webcam snapshot"
echo "  /octoclaw telegram  - Send status to Telegram"
echo ""
echo "For more info, see: https://github.com/yourusername/octoclaw"
