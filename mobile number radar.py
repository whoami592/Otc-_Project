#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#   MOBILE NUMBER RADAR v1.0
#   Coded By: Cyber Security Engineer Mr. Sabaz Ali Khan
# ============================================================

import sys, time, os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from colorama import init, Fore, Style

init(autoreset=True)

# ---------------- COLORS ----------------
RED    = Fore.RED
GREEN  = Fore.GREEN
YELLOW = Fore.YELLOW
CYAN   = Fore.CYAN
MAGENTA= Fore.MAGENTA
WHITE  = Fore.WHITE
BOLD   = Style.BRIGHT
RESET  = Style.RESET_ALL

BANNER = r"""
  ██     ██  ██████   ██████  ██   ██ ██    ██  ███████
   ██   ██ ██     ██ ██      ██  ██  ██    ██ ██ 
    ██████  ██     ██ ██      █████    ██  ██  ███████
            ██     ██ ██      ██  ██    ██   ██        ██
      ██      ██████    ██████ ██   ██    ████  ███████
                  MOBILE NUMBER RADAR v1.0
"""

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def animate_banner():
    """Matrix-style animated banner"""
    clear()
    banner_lines = BANNER.split("\n")
    colors = [MAGENTA, CYAN, GREEN, YELLOW, RED, WHITE, MAGENTA, CYAN, GREEN, YELLOW, RED, WHITE, MAGENTA]
    for i, line in enumerate(banner_lines):
        print(colors[i % len(colors)] + BOLD + line.center(70) + RESET)
        time.sleep(0.05)
    print(CYAN + BOLD + "=" * 70 + RESET)
    print(GREEN + BOLD + "   [+] TOOL      : MOBILE NUMBER RADAR".center(80) + RESET)
    print(GREEN + BOLD + "   [+] VERSION   : 1.0".center(80) + RESET)
    print(MAGENTA + BOLD + "   [+] CODED BY  : CYBER SECURITY ENGINEER MR. SABAZ ALI KHAN".center(80) + RESET)
    print(MAGENTA + BOLD + "   [+] TEAM      : ANONYMOUS x MIRTX STYLE".center(80) + RESET)
    print(RED    + BOLD + "   [+] WARNING   : SIRF AUTHORIZED / EDUCATIONAL PURPOSE KE LIYE!".center(80) + RESET)
    print(CYAN + BOLD + "=" * 70 + RESET)

def scanning_animation(number):
    """Fake radar scan animation"""
    frames = ["|", "/", "-", "\\"]
    for i in range(20):
        frame = frames[i % 4]
        sys.stdout.write(YELLOW + f"\r    [*] RADAR SCANNING {number} ... {frame}  " + RESET)
        sys.stdout.flush()
        time.sleep(0.08)
    print(GREEN + "\r    [+] SCAN COMPLETE!                                    " + RESET)

def radar_scan(number):
    """Phone number OSINT analysis"""
    try:
        parsed = phonenumbers.parse(number, None)
    except Exception as e:
        print(RED + f"    [-] ERROR: Invalid number format! ({e})" + RESET)
        return

    print(CYAN + "\n    ═════════════ RADAR RESULTS ═════════════" + RESET)

    if not phonenumbers.is_valid_number(parsed):
        print(RED + "    [-] INVALID NUMBER — Radar lock FAIL!" + RESET)
        return

    tz = timezone.time_zones_for_number(parsed)
    operator = carrier.name_for_number(parsed, "en")
    location = geocoder.description_for_number(parsed, "en")
    national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    intl     = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    e164     = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    region   = phonenumbers.region_code_for_number(parsed)
    ntype    = phonenumbers.number_type(parsed)
    ntypes = {0:"FIXED LINE",1:"MOBILE",2:"FIXED LINE OR MOBILE",3:"TOLL FREE",
              4:"PREMIUM RATE",5:"SHARED COST",6:"VOIP",7:"PERSONAL NUMBER",
              8:"PAGER",9:"UAN",10:"VOICEMAIL",11:"UNKNOWN"}

    data = [
        ("TARGET NUMBER",   intl),
        ("E.164 FORMAT",    e164),
        ("NATIONAL FORMAT", national),
        ("VALID STATUS",    "VALID ✔" ),
        ("POSSIBLE",        "YES ✔" if phonenumbers.is_possible_number(parsed) else "NO ✘"),
        ("CARRIER / OPERATOR", operator if operator else "UNKNOWN"),
        ("REGION / COUNTRY",  f"{location} | {region}"),
        ("TIME ZONE",         ", ".join(tz)),
        ("NUMBER TYPE",       ntypes.get(ntype, "UNKNOWN")),
    ]
    for label, value in data:
        print(GREEN + f"    [+] {label:<20} : " + YELLOW + BOLD + f"{value}" + RESET)

    print(CYAN + "    ══════════════════════════════════════════" + RESET)

def main():
    animate_banner()
    while True:
        print(YELLOW + "\n    [1] SCAN MOBILE NUMBER" + RESET)
        print(YELLOW + "    [2] CLEAR SCREEN" + RESET)
        print(RED    + "    [0] EXIT RADAR" + RESET)
        choice = input(CYAN + "\n    [ROOT@RADAR]~$ " + RESET).strip()

        if choice == "1":
            number = input(WHITE + "    [?] ENTER MOBILE NUMBER (with country code, e.g +92300xxxxxxx): " + RESET).strip()
            if number:
                scanning_animation(number)
                radar_scan(number)
        elif choice == "2":
            animate_banner()
        elif choice == "0":
            print(RED + BOLD + "\n    [!] RADAR SHUTTING DOWN... STAY ANONYMOUS! ✔\n" + RESET)
            sys.exit(0)
        else:
            print(RED + "    [-] INVALID OPTION!" + RESET)

if __name__ == "__main__":
    main()
