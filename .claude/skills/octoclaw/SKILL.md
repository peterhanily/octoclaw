---
name: octoclaw
description: Control Octoprint 3D printer - check status, start prints, upload files, monitor jobs. Use when user wants to interact with their 3D printer.
argument-hint: [command]
user-invocable: true
allowed-tools: Bash, Read, Write
---

# OctoClaw - Octoprint Control Skill

You are now controlling an Octoprint 3D printer instance. Use the helper script to interact with the Octoprint API.

## Available Commands

The helper script is located at: `~/.claude/skills/octoclaw/scripts/octoprint.py`

### Check Printer Status
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py status
```
Returns current printer state, temperatures, and active job information.

### List Available Files
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py list-files
```
Lists all gcode files available on the Octoprint instance.

### Upload a File
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py upload <local-filepath> [remote-filename]
```
Uploads a gcode file to Octoprint.

### Start a Print
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py print <filename>
```
Starts printing the specified file (must already be on Octoprint).

### Control Print Job
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py control <pause|resume|cancel>
```
Pause, resume, or cancel the current print job.

### Set Temperature
```bash
python3 ~/.claude/skills/octoclaw/scripts/octoprint.py temp <tool0|bed> <temperature>
```
Set temperature for the hotend (tool0) or heated bed.

## Workflow

When the user wants to print something:

1. **Check Status First**: Always check printer status to ensure it's ready
2. **List Files**: If they want to print an existing file, list available files
3. **Upload if Needed**: If printing a local file, upload it first
4. **Start Print**: Select and start the print job
5. **Monitor**: You can check status periodically to monitor progress

## Common Tasks

### Print a Benchy
If the user wants to print a benchy (3D printer test model):
1. Check if benchy.gcode exists in the files
2. If not, inform the user they need to provide a benchy.gcode file or download one
3. Upload the file if provided
4. Start the print

### Check Print Progress
Parse the status output to show:
- Current state (Printing, Operational, etc.)
- Print progress percentage
- Time remaining
- Current temperatures

### Emergency Stop
Use the `control cancel` command to stop a print immediately.

## Response Format

When showing printer status, format the output in a user-friendly way:
- **State**: Operational/Printing/Paused
- **Temperatures**: Tool: X°C / Bed: Y°C
- **Progress**: X% complete, Y minutes remaining
- **Current File**: filename.gcode

## Error Handling

If the helper script fails:
1. Check that config.json exists and has valid credentials
2. Verify the Octoprint instance is reachable
3. Confirm the API key is correct
4. Make sure the printer is powered on and connected

## Arguments

When invoked with arguments (e.g., `/octoclaw status`), use $ARGUMENTS to determine the requested action.

Examples:
- `/octoclaw status` → Check printer status
- `/octoclaw files` → List files
- `/octoclaw print benchy.gcode` → Start printing benchy

If no arguments provided, ask the user what they'd like to do with their printer.
