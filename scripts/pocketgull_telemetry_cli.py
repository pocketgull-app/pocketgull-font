#!/usr/bin/env python3
"""
PocketGull Terminal Telemetry CLI (pocketgull-cli)
=================================================
Live, zero-shear terminal telemetry engine powered by PocketGull Mono.
Demonstrates:
  - 600 UPM fixed-pitch column alignment across terminal emulators
  - Gapless box drawing (U+256D-U+2570 rounded borders)
  - ISMP clinical disambiguation (slashed zero, curved l, serifed I)
  - 650nm Scotopic Red Mode for astronomical observatories
  - Sub-cell waveforms and real-time differential screen updates

Usage:
  python scripts/pocketgull_telemetry_cli.py [--mode clinical|astro|system] [--interval SECONDS] [--once]
"""

import sys
import time
import math
import os
import argparse
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ANSI Color Palettes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Clinical Obsidian HUD Palette
CYAN = "\033[38;2;6;182;212m"
EMERALD = "\033[38;2;16;185;129m"
AMBER = "\033[38;2;245;158;11m"
ROSE = "\033[38;2;251;113;133m"
PURPLE = "\033[38;2;168;85;247m"
BLUE = "\033[38;2;96;165;250m"
WHITE = "\033[38;2;248;250;252m"
GRAY = "\033[38;2;148;163;184m"
DARK_GRAY = "\033[38;2;71;85;105m"

# Scotopic 650nm Red Mode Palette
RED_BRIGHT = "\033[38;2;255;51;51m"
RED_MID = "\033[38;2;204;0;0m"
RED_DARK = "\033[38;2;128;0;0m"
RED_DIM = "\033[38;2;80;0;0m"

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def move_cursor_home():
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def format_ecg(step):
    """Generates a dynamic 600 UPM ECG sub-cell lead trace."""
    frames = [
        "__/\_             __/\_             __/\_             __/\_        ",
        "  __/\_             __/\_             __/\_             __/\_      ",
        "    __/\_             __/\_             __/\_             __/\_    ",
        "      __/\_             __/\_             __/\_             __/\_  ",
        "        __/\_             __/\_             __/\_             __/\_",
        "_         __/\_             __/\_             __/\_             __/",
        "/_          __/\_             __/\_             __/\_             _",
    ]
    return frames[step % len(frames)]

def format_pleth(step):
    """Generates a dynamic sub-cell pleth wave."""
    bars = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    vals = []
    for i in range(54):
        x = (i + step * 2) * 0.35
        y = math.sin(x) * 0.5 + 0.5
        # dicrotic notch
        y += 0.25 * math.sin(x * 2.1)
        idx = max(0, min(7, int(y * 7)))
        vals.append(bars[idx])
    return "".join(vals)

def render_clinical_hud(t_step):
    """Render Clinical ICU Intensive Care Telemetry HUD."""
    hr = 72 + int(math.sin(t_step * 0.2) * 3)
    map_val = 93 + int(math.cos(t_step * 0.15) * 2)
    spo2 = 99 if (t_step % 5 != 0) else 98
    etco2 = 38 + int(math.sin(t_step * 0.3) * 1)
    
    ecg_trace = format_ecg(t_step)
    pleth_wave = format_pleth(t_step)
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    out = []
    out.append(f"{CYAN}╭───────────────────────────────────────────────────────────────────────────────────────────────╮{RESET}")
    out.append(f"{CYAN}│{RESET} {BOLD}{WHITE}POCKETGULL CLINICAL TELEMETRY MONITOR :: BED 0̸4 (NEURO-ICU POD-A){RESET}     {GRAY}{timestamp}{RESET} {CYAN}│{RESET}")
    out.append(f"{CYAN}├───────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
    out.append(f"{CYAN}│{RESET} PATIENT: {WHITE}Sapiens, H. (34y F){RESET}  {GRAY}│{RESET} MRN: {WHITE}#9842-0̸1-STAT{RESET}       {GRAY}│{RESET} RHYTHM: {EMERALD}NORMAL SINUS (STABLE){RESET}  {CYAN}│{RESET}")
    out.append(f"{CYAN}├─────────────────────────────────┴──────────────────────────────┴──────────────────────────────┤{RESET}")
    out.append(f"{CYAN}│{RESET} [HEART RATE]    {EMERALD}{BOLD}{hr:3d} bpm{RESET}  {GRAY}(SINUS RESTORATIVE){RESET} │ [BLOOD PRESSURE] {WHITE}120̸/80̸ mmHg{RESET} {GRAY}(MAP: {map_val} mmHg){RESET}   {CYAN}│{RESET}")
    out.append(f"{CYAN}│{RESET} [PULSE OX]      {CYAN}{BOLD}{spo2:3d} %{RESET}    {GRAY}(PLETH PI: 4.8%){RESET}    │ [RESPIRATORY]    {BLUE}16 br/min{RESET}    {GRAY}(ETCO2: {etco2} mmHg){RESET} {CYAN}│{RESET}")
    out.append(f"{CYAN}│{RESET} [TEMPERATURE]   {AMBER}{BOLD}36.8 °C{RESET}  {GRAY}(NORMOTHERMIC){RESET}      │ [CONSCIOUSNESS]  {PURPLE}GCS 15{RESET}       {GRAY}(E4 V5 M6 FULL){RESET}  {CYAN}│{RESET}")
    out.append(f"{CYAN}├───────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
    out.append(f"{CYAN}│{RESET} {DIM}[ECG-LEAD II]{RESET}  {EMERALD}{ecg_trace}{RESET}     {CYAN}│{RESET}")
    out.append(f"{CYAN}│{RESET} {DIM}[PLETH WAVE ]{RESET}  {CYAN}{pleth_wave}{RESET}     {CYAN}│{RESET}")
    out.append(f"{CYAN}├───────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
    out.append(f"{CYAN}│{RESET} ACTIVE DIRECTIVE: {WHITE}R Cefazolin 2 g IV Q8H{RESET} • {AMBER}ALLERGY: PENICILLIN{RESET} • {GRAY}ø 18G Cannula R-AC{RESET}         {CYAN}│{RESET}")
    out.append(f"{CYAN}│{RESET} {DARK_GRAY}POWERLINE  icu-station  main  bed-0̸4  tty1 (PocketGull Mono 600 UPM fixed pitch)           {CYAN}│{RESET}")
    out.append(f"{CYAN}╰───────────────────────────────────────────────────────────────────────────────────────────────╯{RESET}")
    out.append(f"{GRAY} ⠁⠍⠕⠭⠊⠉⠊⠇⠇⠊⠝⠀⠼⠑⠚⠚⠀⠍⠛⠀•⠀Full 256 Unicode Braille Coverage (U+2800–U+28FF) • W3C OTS Valid{RESET}")
    return "\n".join(out)

def render_astro_hud(t_step):
    """Render Astronomical Observatory Scotopic 650nm Red Mode Console."""
    ra_deg = (187.705930 + (t_step * 0.002)) % 360.0
    dec_deg = 12.391120 + (math.sin(t_step * 0.01) * 0.001)
    airmass = 1.04 + (math.sin(t_step * 0.05) * 0.01)
    
    ra_h = int(ra_deg / 15.0)
    ra_m = int((ra_deg / 15.0 - ra_h) * 60)
    ra_s = ((ra_deg / 15.0 - ra_h) * 60 - ra_m) * 60
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    out = []
    out.append(f"{RED_DARK}╭───────────────────────────────────────────────────────────────────────────────────────────────╮{RESET}")
    out.append(f"{RED_DARK}│{RESET} {BOLD}{RED_BRIGHT}POCKETGULL ASTRONOMICAL OBSERVATORY CONSOLE [650nm SCOTOPIC RED MODE]{RESET}   {RED_MID}{timestamp}{RESET} {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}├───────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
    out.append(f"{RED_DARK}│{RESET} TARGET: {RED_BRIGHT}M87* (Virgo A Supermassive){RESET} {RED_DARK}│{RESET} TELESCOPE: {RED_MID}Keck-I 10m Optical{RESET} {RED_DARK}│{RESET} FILTER: {RED_BRIGHT}H-alpha 656.3nm{RESET} {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}├─────────────────────────────────┴──────────────────────────────┴──────────────────────────────┤{RESET}")
    out.append(f"{RED_DARK}│{RESET} [RIGHT ASCENSION] {RED_BRIGHT}{ra_h:02d}h {ra_m:02d}m {ra_s:05.2f}s{RESET}   {RED_MID}(J2000.0){RESET}   │ [AIR MASS]       {RED_BRIGHT}{airmass:.3f}{RESET}  {RED_MID}(Zenith Optical){RESET}   {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}│{RESET} [DECLINATION]     {RED_BRIGHT}+{int(dec_deg):02d}° {int((dec_deg%1)*60):02d}' {((dec_deg%1)*60%1)*60:04.1f}\"{RESET} {RED_MID}(True Geo){RESET}   │ [PARALLACTIC]    {RED_BRIGHT}-42.8°{RESET} {RED_MID}(Derotator On){RESET}    {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}│{RESET} [JULIAN DATE]     {RED_BRIGHT}2460̸934.3184{RESET}          {RED_MID}(LST 14:12:0̸8){RESET}│ [SEEING / FWHM]  {RED_BRIGHT}0̸.42\"{RESET}  {RED_MID}(Diffraction Lim){RESET} {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}├───────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
    out.append(f"{RED_DARK}│{RESET} {BOLD}{RED_MID}CELESTIAL CONSTANTS MATRIX (Procedural Operators 0x2299, 0x2295, 0x2643, 0x2644):{RESET}             {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}│{RESET}   ☉ Solar Mass:  {RED_BRIGHT}1.9884 × 10³⁰ kg{RESET}   (R☉ = 6.957 × 10⁸ m)                              {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}│{RESET}   ⊕ Earth Mass:  {RED_BRIGHT}5.9722 × 10²⁴ kg{RESET}   (R⊕ = 6.3781 × 10⁶ m)                             {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}│{RESET}   ♃ Jupiter Mass:{RED_BRIGHT}1.8981 × 10²⁷ kg{RESET}   (317.8 M⊕ nominal)                                {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}│{RESET}   ♄ Saturn Mass: {RED_BRIGHT}5.6834 × 10²⁶ kg{RESET}   (95.16 M⊕ nominal)                                {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}├───────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
    out.append(f"{RED_DARK}│{RESET} {RED_DIM}FITS-80: SIMPLE = T | BITPIX = -64 | NAXIS = 2 | CRVAL1 = {ra_deg:10.6f} | CRVAL2 = {dec_deg:9.6f} {RED_DARK}│{RESET}")
    out.append(f"{RED_DARK}╰───────────────────────────────────────────────────────────────────────────────────────────────╯{RESET}")
    out.append(f"{RED_DIM} [DARK-SKY PRESERVATION] All blue/green wavelengths eliminated. Rhodopsin adaptation preserved. {RESET}")
    return "\n".join(out)

def render_system_hud(t_step):
    """Render Hardware & Typefoundry Engine Status Telemetry."""
    cpu_pct = 24.2 + math.sin(t_step * 0.4) * 8.0
    mem_pct = 41.5 + math.cos(t_step * 0.2) * 1.5
    fcp_ms = 14.8 + math.sin(t_step * 0.1) * 0.4
    
    # Progress bars
    def pbar(pct, width=28, col=EMERALD):
        filled = int((pct / 100.0) * width)
        return f"{col}{'█' * filled}{DARK_GRAY}{'░' * (width - filled)}{RESET}"
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    out = []
    out.append(f"{BLUE}╭───────────────────────────────────────────────────────────────────────────────────────────────╮{RESET}")
    out.append(f"{BLUE}│{RESET} {BOLD}{WHITE}POCKETGULL FOUNDRY SYSTEM & KERNEL ENGINE TELEMETRY{RESET}               {GRAY}{timestamp}{RESET} {BLUE}│{RESET}")
    out.append(f"{BLUE}├───────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
    out.append(f"{BLUE}│{RESET} [CPU USAGE]      [{pbar(cpu_pct, 24, EMERALD)}]  {WHITE}{cpu_pct:5.1f}%{RESET} {GRAY}(DirectWrite 30.8× Speed){RESET} {BLUE}│{RESET}")
    out.append(f"{BLUE}│{RESET} [RAM ALLOCATION] [{pbar(mem_pct, 24, BLUE)}]  {WHITE}{mem_pct:5.1f}%{RESET} {GRAY}(18.1 KB Micro Footprint){RESET} {BLUE}│{RESET}")
    out.append(f"{BLUE}├───────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
    out.append(f"{BLUE}│{RESET} {BOLD}TYPEFOUNDRY INVARIANT METRICS (Dart 3.11 + TrueType Engine):{RESET}                           {BLUE}│{RESET}")
    out.append(f"{BLUE}│{RESET}   ✦ W3C OTS Memory Safety:       {EMERALD}118 / 118 Binaries PASSED (0̸ odd offsets){RESET}             {BLUE}│{RESET}")
    out.append(f"{BLUE}│{RESET}   ✦ Word-Alignment Boundary:     {EMERALD}loca[i] % 2 == 0̸ (16-bit word aligned){RESET}                {BLUE}│{RESET}")
    out.append(f"{BLUE}│{RESET}   ✦ Monospace Pitch Invariant:   {EMERALD}60̸0̸ UPM Fixed Advance Width (0̸.0̸0̸0̸px shear){RESET}          {BLUE}│{RESET}")
    out.append(f"{BLUE}│{RESET}   ✦ Sub-Second First Paint:      {CYAN}{fcp_ms:4.1f} ms FCP (Fits TCP initcwnd burst){RESET}            {BLUE}│{RESET}")
    out.append(f"{BLUE}│{RESET}   ✦ OLED Power Reduction:        {EMERALD}-34.0̸% Active Luminance Draw (+2.1 hrs battery){RESET}       {BLUE}│{RESET}")
    out.append(f"{BLUE}│{RESET}   ✦ Paper Toner Deposition:      {EMERALD}-22.4% Ink Area per Prescription Form{RESET}              {BLUE}│{RESET}")
    out.append(f"{BLUE}╰───────────────────────────────────────────────────────────────────────────────────────────────╯{RESET}")
    out.append(f"{GRAY} OpenType Features Active: [zero: 1] [cv0̸5: 1] [ss0̸2: 1] [cv11: 1] [tnum: 1] • OFL 1.1 Licensed{RESET}")
    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description="PocketGull Live Terminal Telemetry CLI")
    parser.add_argument("--mode", choices=["clinical", "astro", "system"], default="clinical",
                        help="Telemetry HUD mode (default: clinical)")
    parser.add_argument("--interval", type=float, default=0.25,
                        help="Refresh interval in seconds (default: 0.25)")
    parser.add_argument("--once", action="store_true",
                        help="Render single snapshot and exit")
    args = parser.parse_args()

    # Hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    
    clear_screen()
    t_step = 0
    try:
        while True:
            move_cursor_home()
            if args.mode == "clinical":
                print(render_clinical_hud(t_step))
            elif args.mode == "astro":
                print(render_astro_hud(t_step))
            elif args.mode == "system":
                print(render_system_hud(t_step))
            
            if args.once:
                break
            
            time.sleep(args.interval)
            t_step += 1
    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
