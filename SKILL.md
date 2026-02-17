---
name: octoclaw
description: Control Octoprint 3D printer - monitor status with formatting, capture webcam snapshots, analyze gcode, detect errors, and send Telegram notifications. Use when user wants to interact with their 3D printer.
argument-hint: [command]
user-invocable: true
allowed-tools: Bash, Read, Write
---

# OctoClaw - Enhanced Octoprint Control Skill

You are now controlling an Octoprint 3D printer instance with advanced monitoring, analysis, and notification capabilities.

## Helper Script Location

`$SKILL_DIR/scripts/octoprint.py`

## Core Commands

### Status & Monitoring

**Get Formatted Status** (Recommended for user display)
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py status-pretty
```
Shows beautifully formatted status with:
- Color-coded printer state
- Temperature readouts with status indicators
- Progress bar for active prints
- Time elapsed, remaining, and ETA
- Filament usage estimates

**Get Raw Status JSON**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py status
```
Returns raw JSON for parsing.

**Check for Errors**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py check-errors
```
Monitors for:
- Printer error states
- Temperature anomalies (deviation from target, overheating)
- Connection issues
- Stalled prints
Returns JSON with errors/warnings array.

### File Management

**List Files**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py list-files
```

**Upload File**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py upload <local-filepath> [remote-filename]
```

**Analyze GCode**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py analyze <filepath>
```
Extracts metadata from gcode files:
- Layer count
- Estimated print time
- Filament length/volume
- Bed and hotend temperatures
- Bounding box dimensions

### Print Control

**Start Print**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py print <filename>
```

**Control Print**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py control <pause|resume|cancel>
```

**Set Temperature**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py temp <tool0|bed> <temperature>
```

### Webcam Features

**Capture Snapshot**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py snapshot [output-path]
```
Captures current webcam image. If no path provided, saves to /tmp with timestamp.

### Telegram Integration

**Send Status to Telegram**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py telegram-status
```
Sends formatted status message to configured Telegram chat.

**Send Snapshot to Telegram**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py telegram-snapshot
```
Captures and sends webcam snapshot with progress caption to Telegram.

**Send Custom Message**
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py telegram-msg "Your message here"
```
Sends arbitrary message to Telegram (supports Markdown formatting).

## Workflow Examples

### Monitor Active Print
1. Use `status-pretty` to show formatted status with progress
2. Optionally capture snapshot to see current state
3. Use `check-errors` to verify no issues
4. Send snapshot to Telegram for remote monitoring

### Start New Print
1. Check printer state with `status-pretty`
2. Ensure printer is Operational (not printing/error)
3. List files or upload new gcode
4. Optionally analyze gcode to show estimates
5. Start print
6. Send Telegram notification that print started

### Troubleshoot Issues
1. Run `check-errors` to identify problems
2. Check temperatures are reaching target
3. Verify printer connection status
4. Capture snapshot to visually inspect
5. Send diagnostic info to Telegram

### Remote Monitoring
1. Periodically send snapshots to Telegram
2. Send status updates at milestones (25%, 50%, 75%)
3. Alert on errors or completion
4. Provide ETA estimates

## Response Formatting

When showing status to users:
- Use `status-pretty` for terminal display (includes colors and formatting)
- Parse `status` JSON when you need programmatic access
- Always show progress percentage, time remaining, and ETA for active prints
- Include temperature info (actual/target)
- Mention filament usage if available

## Telegram Setup

To enable Telegram features, the config.json must include:
1. `telegram_bot_token` - Get from @BotFather on Telegram
2. `telegram_chat_id` - Your chat ID with the bot

To create a bot:
1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Follow prompts to name your bot
4. Copy the bot token to config.json

To get your chat ID:
1. Message your bot
2. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Find your chat ID in the response

## Error Handling

The skill will automatically detect:
- **Critical errors**: Printer error state, connection lost, extreme temperature deviations (>15°C)
- **Warnings**: Moderate temperature deviations (5-15°C), potential stalled prints

When errors detected, recommend:
1. Send error details to Telegram for immediate alert
2. Capture snapshot to assess situation
3. Pause print if temperature deviation detected
4. Cancel print if critical error

## Arguments

When invoked with arguments, use $ARGUMENTS to route commands:

- `/octoclaw status` → Show pretty formatted status
- `/octoclaw check` → Run error check
- `/octoclaw snapshot` → Capture and show snapshot path
- `/octoclaw telegram` → Send status to Telegram
- `/octoclaw telegram snap` → Send snapshot to Telegram
- `/octoclaw print <file>` → Start printing
- `/octoclaw pause` → Pause print
- `/octoclaw resume` → Resume print
- `/octoclaw cancel` → Cancel print
- `/octoclaw analyze <file>` → Analyze gcode file

If no arguments provided, show formatted status by default.

## Best Practices

1. **Always check status before starting prints**
2. **Use error monitoring during long prints** - Periodically run `check-errors`
3. **Send Telegram notifications for important events** - Print start/finish, errors
4. **Capture snapshots at milestones** - Beginning, 50%, completion
5. **Analyze gcode before printing** - Give users time estimates and filament requirements
6. **Format output appropriately** - Use pretty status for humans, JSON for parsing
