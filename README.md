# OctoClaw - Octoprint Skill for Claude Code

A Claude Code skill for controlling Octoprint 3D printers.

## Features

- Print files from Octoprint
- Check printer status
- Monitor print progress
- Control temperature
- Start/stop/pause prints

## Installation

1. Copy the skill to your Claude skills directory:
```bash
cp -r .claude/skills/octoclaw ~/.claude/skills/
```

2. Configure your Octoprint connection:
```bash
cp .claude/skills/octoclaw/config.example.json .claude/skills/octoclaw/config.json
```

3. Edit `~/.claude/skills/octoclaw/config.json` with your Octoprint details:
   - IP address
   - API key (found in Octoprint Settings > API)

## Usage

Use `/octoclaw` in Claude Code to interact with your 3D printer:

```
/octoclaw status
/octoclaw print benchy.gcode
/octoclaw list-files
```

## Requirements

- Octoprint instance running on your network
- Octoprint API key
- Python 3.x with requests library (for helper scripts)
