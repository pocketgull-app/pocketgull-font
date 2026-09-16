#!/usr/bin/env python3
"""
PocketGull: Windows Terminal Theme Installer
Safely injects 'PocketGull Healing Cinema' and 'PocketGull 670nm Retinal PBM'
into Windows Terminal LocalState/settings.json with an automatic backup.
"""

import json
import os
import shutil
import glob

def find_wt_settings():
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    pattern = os.path.join(local_app_data, "Packages", "*WindowsTerminal*", "LocalState", "settings.json")
    matches = glob.glob(pattern)
    if matches:
        return matches[0]
    
    # Fallback standard path
    std_path = os.path.join(local_app_data, "Microsoft", "Windows Terminal", "settings.json")
    if os.path.exists(std_path):
        return std_path
    return None

def main():
    settings_path = find_wt_settings()
    if not settings_path:
        print("[ERROR] Windows Terminal settings.json not found.")
        return

    print(f"[FOUND] Windows Terminal Settings: {settings_path}")
    
    # Backup
    bak_path = settings_path + ".bak"
    shutil.copy2(settings_path, bak_path)
    print(f"[BACKUP] Saved backup to {bak_path}")

    with open(settings_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "schemes" not in data:
        data["schemes"] = []

    # Filter out existing pocketgull schemes if already present
    data["schemes"] = [s for s in data["schemes"] if not s.get("name", "").startswith("PocketGull")]

    # PocketGull Schemes
    healing_cinema_scheme = {
        "name": "PocketGull Healing Cinema",
        "background": "#050811",
        "foreground": "#E2E8F0",
        "cursorColor": "#2DD4BF",
        "selectionBackground": "#1E293B",
        "black": "#0F172A",
        "red": "#F87171",
        "green": "#2DD4BF",
        "yellow": "#FBBF24",
        "blue": "#38BDF8",
        "purple": "#C084FC",
        "cyan": "#22D3EE",
        "white": "#F1F5F9",
        "brightBlack": "#475569",
        "brightRed": "#FCA5A5",
        "brightGreen": "#5EEAD4",
        "brightYellow": "#FDE047",
        "brightBlue": "#7DD3FC",
        "brightPurple": "#E9D5FF",
        "brightCyan": "#67E8F9",
        "brightWhite": "#FFFFFF"
    }

    pbm_scheme = {
        "name": "PocketGull 670nm Retinal PBM",
        "background": "#0A0303",
        "foreground": "#FED7AA",
        "cursorColor": "#FB923C",
        "selectionBackground": "#2A1010",
        "black": "#1C0A0A",
        "red": "#EF4444",
        "green": "#F97316",
        "yellow": "#FBBF24",
        "blue": "#EA580C",
        "purple": "#E11D48",
        "cyan": "#FB923C",
        "white": "#FFEDD5",
        "brightBlack": "#7F1D1D",
        "brightRed": "#F87171",
        "brightGreen": "#FB923C",
        "brightYellow": "#FDE047",
        "brightBlue": "#F97316",
        "brightPurple": "#FDA4AF",
        "brightCyan": "#FED7AA",
        "brightWhite": "#FFFFFF"
    }

    data["schemes"].append(healing_cinema_scheme)
    data["schemes"].append(pbm_scheme)

    # Check if dedicated PocketGull profile exists
    profiles = data.get("profiles", {}).get("list", [])
    has_pg_profile = any(p.get("name") == "PocketGull Telemetry Console" for p in profiles)
    
    if not has_pg_profile:
        pg_profile = {
            "guid": "{a044dcc9-38cf-405f-9505-ace403f4517c}",
            "name": "PocketGull Telemetry Console",
            "commandline": "powershell.exe",
            "colorScheme": "PocketGull Healing Cinema",
            "font": {
                "face": "Pocket Gull Mono",
                "size": 11.5,
                "weight": "medium",
                "features": {
                    "cv08": 1,
                    "ss02": 1,
                    "cv05": 1,
                    "cv11": 1
                }
            },
            "acrylicOpacity": 0.92,
            "useAcrylic": True
        }
        profiles.append(pg_profile)
        print("[ADDED] PocketGull Telemetry Console profile added to Windows Terminal.")

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("[SUCCESS] PocketGull Healing Cinema & 670nm PBM schemes successfully registered in Windows Terminal!")

if __name__ == '__main__':
    main()
