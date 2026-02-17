#!/usr/bin/env python3
"""
Helper script for interacting with Octoprint API
"""
import json
import sys
import os
import requests
from pathlib import Path

def load_config():
    """Load Octoprint configuration"""
    config_path = Path(__file__).parent.parent / "config.json"
    if not config_path.exists():
        print(f"Error: Configuration file not found at {config_path}", file=sys.stderr)
        print("Please copy config.example.json to config.json and fill in your details", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        return json.load(f)

def make_request(method, endpoint, **kwargs):
    """Make a request to Octoprint API"""
    config = load_config()
    url = f"{config['octoprint_url']}{endpoint}"
    headers = {"X-Api-Key": config["api_key"]}

    if "headers" in kwargs:
        kwargs["headers"].update(headers)
    else:
        kwargs["headers"] = headers

    try:
        response = requests.request(method, url, **kwargs, timeout=10)
        response.raise_for_status()
        return response.json() if response.text else {}
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Octoprint: {e}", file=sys.stderr)
        sys.exit(1)

def get_status():
    """Get printer status"""
    printer = make_request("GET", "/api/printer")
    job = make_request("GET", "/api/job")
    connection = make_request("GET", "/api/connection")

    print(json.dumps({
        "printer": printer,
        "job": job,
        "connection": connection
    }, indent=2))

def list_files():
    """List available files"""
    data = make_request("GET", "/api/files?recursive=true")
    files = []

    def extract_files(items, path=""):
        for item in items:
            if item["type"] == "folder":
                extract_files(item.get("children", []), f"{path}{item['name']}/")
            else:
                files.append({
                    "name": item["name"],
                    "path": f"{path}{item['name']}",
                    "size": item.get("size", 0),
                    "date": item.get("date", 0)
                })

    extract_files(data.get("files", []))
    print(json.dumps(files, indent=2))

def start_print(filepath):
    """Start printing a file"""
    # Select the file
    make_request("POST", f"/api/files/local/{filepath}", json={"command": "select"})
    # Start the print
    make_request("POST", "/api/job", json={"command": "start"})
    print(f"Started printing {filepath}")

def control_print(command):
    """Control print job (pause, resume, cancel)"""
    valid_commands = ["pause", "resume", "cancel"]
    if command not in valid_commands:
        print(f"Error: Invalid command. Must be one of {valid_commands}", file=sys.stderr)
        sys.exit(1)

    make_request("POST", "/api/job", json={"command": command})
    print(f"Print {command}ed")

def set_temperature(tool, temp):
    """Set tool or bed temperature"""
    if tool == "bed":
        make_request("POST", "/api/printer/bed", json={"command": "target", "target": int(temp)})
    else:
        make_request("POST", "/api/printer/tool", json={"command": "target", "targets": {tool: int(temp)}})
    print(f"Set {tool} temperature to {temp}°C")

def upload_file(filepath, filename=None):
    """Upload a gcode file to Octoprint"""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if filename is None:
        filename = os.path.basename(filepath)

    config = load_config()
    url = f"{config['octoprint_url']}/api/files/local"
    headers = {"X-Api-Key": config["api_key"]}

    with open(filepath, 'rb') as f:
        files = {'file': (filename, f, 'application/octet-stream')}
        response = requests.post(url, headers=headers, files=files, timeout=30)
        response.raise_for_status()

    print(f"Uploaded {filename} successfully")
    return filename

def main():
    if len(sys.argv) < 2:
        print("Usage: octoprint.py <command> [args...]", file=sys.stderr)
        print("Commands: status, list-files, print <file>, control <pause|resume|cancel>, temp <tool|bed> <temp>, upload <filepath>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        get_status()
    elif command == "list-files":
        list_files()
    elif command == "print":
        if len(sys.argv) < 3:
            print("Error: Missing filename", file=sys.stderr)
            sys.exit(1)
        start_print(sys.argv[2])
    elif command == "control":
        if len(sys.argv) < 3:
            print("Error: Missing control command", file=sys.stderr)
            sys.exit(1)
        control_print(sys.argv[2])
    elif command == "temp":
        if len(sys.argv) < 4:
            print("Error: Missing tool and temperature", file=sys.stderr)
            sys.exit(1)
        set_temperature(sys.argv[2], sys.argv[3])
    elif command == "upload":
        if len(sys.argv) < 3:
            print("Error: Missing filepath", file=sys.stderr)
            sys.exit(1)
        filename = sys.argv[3] if len(sys.argv) > 3 else None
        upload_file(sys.argv[2], filename)
    else:
        print(f"Error: Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
