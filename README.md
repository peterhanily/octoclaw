# OctoClaw - Enhanced Octoprint Skill for Claude Code

A comprehensive Claude Code skill for controlling and monitoring Octoprint 3D printers with advanced features including formatted status displays, webcam snapshots, gcode analysis, error monitoring, and Telegram integration.

## Features

### Phase 1 - Core Enhancements ✅
- **Enhanced Status Display**: Beautiful formatted output with color-coded states, progress bars, and temperature indicators
- **Webcam Snapshot Capture**: Grab images from your printer's webcam
- **GCode Analysis**: Extract metadata including layers, print time, filament usage, and temperatures
- **Error Monitoring**: Automated detection of printer errors, temperature anomalies, and stalled prints

### Phase 2 - Telegram Integration ✅
- **Status Notifications**: Send formatted status updates to Telegram
- **Snapshot Sharing**: Capture and send webcam images with progress info
- **Custom Messages**: Send arbitrary messages to your Telegram chat
- **Remote Monitoring**: Get updates on your prints from anywhere

### Coming Soon (Phase 3)
- Thingiverse/Printables model download integration
- Slicing integration (CuraEngine, PrusaSlicer)
- Smart automation (auto-shutdown, queue management)
- Failure recovery

## Installation

1. Copy the skill to your Claude skills directory:
```bash
cp -r .claude/skills/octoclaw ~/.claude/skills/
```

2. Configure your Octoprint connection:
```bash
cp ~/.claude/skills/octoclaw/config.example.json ~/.claude/skills/octoclaw/config.json
```

3. Edit `~/.claude/skills/octoclaw/config.json` with your settings:
```json
{
  "octoprint_url": "http://octopi.local",
  "api_key": "YOUR_API_KEY_HERE",
  "webcam_url": "http://octopi.local/webcam/?action=snapshot",
  "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
  "telegram_chat_id": "YOUR_TELEGRAM_CHAT_ID"
}
```

### Getting Octoprint API Key
1. Open Octoprint web interface
2. Go to Settings (wrench icon)
3. Navigate to "API" section
4. Copy your API key

### Setting Up Telegram (Optional)
1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Follow prompts to create your bot
4. Copy the bot token to config.json
5. Message your bot
6. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
7. Find your chat ID in the response and add to config.json

## Usage

### Direct Command Usage

**Check printer status (formatted):**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py status-pretty
```

**Capture webcam snapshot:**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py snapshot
```

**Analyze a gcode file:**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py analyze ~/Downloads/benchy.gcode
```

**Check for errors:**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py check-errors
```

**Send status to Telegram:**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py telegram-status
```

**Send snapshot to Telegram:**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py telegram-snapshot
```

**Start a print:**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py print benchy.gcode
```

**Control print (pause/resume/cancel):**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py control pause
```

### Claude Code Skill Usage

Once the skill is installed and Claude Code is restarted, you can use:

```
/octoclaw status        - Show formatted status
/octoclaw snapshot      - Capture webcam snapshot
/octoclaw telegram      - Send status to Telegram
/octoclaw check         - Run error check
/octoclaw print <file>  - Start printing
```

Or simply ask Claude to interact with your printer:
- "Check my 3D printer status"
- "Send me a snapshot of my print on Telegram"
- "Analyze this gcode file and tell me how long it will take"
- "Check if there are any errors with my printer"

## Available Commands

| Command | Description |
|---------|-------------|
| `status` | Get raw status JSON |
| `status-pretty` | Get formatted, color-coded status display |
| `check-errors` | Monitor for errors and anomalies |
| `list-files` | List available gcode files |
| `analyze <file>` | Analyze gcode file metadata |
| `snapshot [path]` | Capture webcam snapshot |
| `print <file>` | Start printing a file |
| `control <cmd>` | Control print (pause/resume/cancel) |
| `temp <tool\|bed> <temp>` | Set temperature |
| `upload <file>` | Upload gcode file |
| `telegram-status` | Send status to Telegram |
| `telegram-snapshot` | Send snapshot to Telegram |
| `telegram-msg <msg>` | Send custom message |

## Status Display Features

The enhanced status display includes:
- **Color-coded state** (Green=Printing, Yellow=Paused, Red=Error, Blue=Operational)
- **Temperature monitoring** with color indicators showing deviation from target
- **Progress bar** for active prints
- **Time tracking**: Elapsed time, remaining time, and ETA
- **Filament usage**: Length in meters and volume in cm³
- **Connection info**: Port, baudrate, and printer profile

## Error Monitoring

Automatic detection of:
- Printer error states
- Connection failures
- Temperature anomalies:
  - Critical: >15°C deviation from target
  - Warning: 5-15°C deviation from target
  - Overheating: >280°C
- Stalled prints (no progress for 5+ minutes)

## GCode Analysis

Extracts from gcode files:
- Total layers
- Estimated print time
- Filament length and volume
- Bed temperature
- Hotend temperature
- Bounding box dimensions
- File size

## Requirements

- Octoprint instance running on your network
- Octoprint API key
- Python 3.x with requests library
- (Optional) Telegram bot for notifications
- (Optional) Webcam connected to Octoprint

## Troubleshooting

**Connection errors:**
- Verify Octoprint URL is correct in config.json
- Check API key is valid
- Ensure Octoprint is running and accessible

**Webcam snapshot fails:**
- Verify webcam_url in config.json
- Check webcam is enabled in Octoprint settings
- Test URL directly in browser

**Telegram not working:**
- Verify bot token and chat ID are correct
- Ensure you've messaged the bot at least once
- Check bot permissions

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## License

MIT

## Credits

Created for use with Claude Code by Anthropic.
Uses the Octoprint REST API for printer control.
