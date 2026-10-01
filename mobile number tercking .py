#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  MOBILE NUMBER TRACKER - OSINT FRAMEWORK v1.0                ║
║  Coded By : Cyber Security Engineer Mr Sabaz Ali Khan        ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import subprocess
from datetime import datetime

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
except ImportError:
    print("[!] phonenumbers library missing... installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "phonenumbers"])
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone

# ===================== COLORS (HACKER STYLE) =====================
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"

# ===================== BANNER =====================
BANNER = f"""{C.RED}{C.BOLD}
   ███╗   ███╗ ██████╗██████╗      ████████╗██████╗  ██████╗ ██╗  ██╗
   ████╗ ████║██╔════╝██╔══██╗     ╚══██╔══╝██╔══██╗██╔═══██╗██║ ██╔╝
   ██╔████╔██║██║     ██████╔╝        ██║   ██████╔╝██║   ██║█████╔╝
   ██║╚██╔╝██║██║     ██╔══██╗        ██║   ██╔══██╗██║   ██║██╔═██╗
   ██║ ╚═╝ ██║╚██████╗██║  ██║        ██║   ██║  ██║╚██████╔╝██║  ██╗
   ╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
{C.CYAN}
      [ >>> MOBILE NUMBER TRACKER :: OSINT FRAMEWORK <<< ]
{C.YELLOW}  ═══════════════════════════════════════════════════════════════════
        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
        █  SOCIAL MEDIA OSINT FRAMEWORK - ALL IN ONE  █
        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
        ██  [+] Phone Number Intelligence             ██
        ██  [+] Carrier / Operator Tracking           ██
        ██  [+] Region & Timezone Lookup              ██
        ██  [+] Line Type Detection                   ██
        ██  [+] Truecaller / Social Media Dorks       ██
        ██  [+] Breach & Leak OSINT Recon             ██
        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  ═══════════════════════════════════════════════════════════════════
{C.GREEN}{C.BOLD}
        [ COD3D BY : CYBER SECURITY ENGINEER MR SABAZ ALI KHAN ]
{C.YELLOW}   >>> WE ARE ANONYMOUS :: WE ARE LEGION :: WE DO NOT FORGIVE <<<
{C.RESET}"""

# ===================== SOCIAL MEDIA OSINT DORKS =====================
SOCIAL_OSINT = [
    ("Truecaller",     "https://www.truecaller.com/search/global/{}"),
    ("WhatsApp Check", "https://wa.me/{}"),
    ("Telegram Check", "https://t.me/+{}"),
    ("Facebook Dork",  "https://www.google.com/search?q=%22{}%22+site:facebook.com"),
    ("Instagram Dork", "https://www.google.com/search?q=%22{}%22+site:instagram.com"),
    ("Twitter/X Dork", "https://www.google.com/search?q=%22{}%22+site:twitter.com+OR+site:x.com"),
    ("LinkedIn Dork",  "https://www.google.com/search?q=%22{}%22+site:linkedin.com"),
    ("Pastebin Leak",  "https://www.google.com/search?q=%22{}%22+site:pastebin.com"),
    ("Breach Dork",    "https://www.google.com/search?q=intext:%22{}%22+(leak+OR+dump+OR+breach)"),
    ("Telegram Dork",  "https://www.google.com/search?q=%22{}%22+site:t.me"),
    ("HaveIBeenPwned", "https://haveibeenpwned.com/"),
    ("Eyecon Search",  "https://eyecon.online/search?q={}"),
]

def typing_print(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def hack_loading():
    frames = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]",
              "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]",
              "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]",
              "[■■■■■■■■■■]"]
    for f in frames:
        sys.stdout.write(f"\r{C.GREEN}  [*] Initializing OSINT Modules {f}{C.RESET}")
        time.sleep(0.15)
    print()

def analyze_number(number):
    print(f"\n{C.CYAN}{C.BOLD}  ╔══[ TARGET ANALYSIS STARTED ]══╗{C.RESET}\n")
    try:
        parsed = phonenumbers.parse(number, None)
    except phonenumbers.NumberParseException as e:
        print(f"{C.RED}  [-] Invalid number format: {e}{C.RESET}")
        return

    if not phonenumbers.is_valid_number(parsed):
        print(f"{C.RED}  [-] Number is NOT valid in any telecom database{C.RESET}")
    else:
        print(f"{C.GREEN}  [+] Number VALID in telecom registry{C.RESET}")

    intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    tz = timezone.time_zones_for_number(parsed)
    reg = geocoder.description_for_number(parsed, "en")
    car = carrier.name_for_number(parsed, "en")
    ntype = phonenumbers.number_type(parsed)
    type_map = {
        0: "FIXED LINE", 1: "MOBILE", 2: "FIXED LINE OR MOBILE",
        3: "TOLL FREE", 4: "PREMIUM RATE", 5: "SHARED COST",
        6: "VOIP (VoIP Number - Possible Virtual/Spoofed)",
        7: "PERSONAL NUMBER", 8: "PAGER", 9: "UAN", 10: "VOICEMAIL"
    }
    cc = parsed.country_code
    nsn = parsed.national_number
    country = phonenumbers.region_code_for_number(parsed)

    print(f"""
  {C.WHITE}{C.BOLD}───────────[ INTELLIGENCE REPORT ]───────────{C.RESET}
  {C.CYAN}[▓]{C.RESET} Number (Intl) : {C.GREEN}{intl}{C.RESET}
  {C.CYAN}[▓]{C.RESET} E.164 Format  : {C.GREEN}{e164}{C.RESET}
  {C.CYAN}[▓]{C.RESET} Country Code  : {C.GREEN}+{cc}{C.RESET}
  {C.CYAN}[▓]{C.RESET} Country/Region: {C.GREEN}{country}{C.RESET}
  {C.CYAN}[▓]{C.RESET} Location      : {C.GREEN}{reg or 'N/A'}{C.RESET}
  {C.CYAN}[▓]{C.RESET} Carrier       : {C.GREEN}{car or 'N/A / MVNO'}{C.RESET}
  {C.CYAN}[▓]{C.RESET} Line Type     : {C.GREEN}{type_map.get(ntype, 'UNKNOWN')}{C.RESET}
  {C.CYAN}[▓]{C.RESET} Timezones     : {C.GREEN}{', '.join(tz) if tz else 'N/A'}{C.RESET}
  {C.CYAN}[▓]{C.RESET} Current Time  : {C.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}
  {C.WHITE}{C.BOLD}──────────────────────────────────────────────{C.RESET}
""")

    print(f"{C.YELLOW}{C.BOLD}  ────[ SOCIAL MEDIA OSINT LINKS ]────{C.RESET}\n")
    for name, url in SOCIAL_OSINT:
        link = url.format(e164.lstrip("+"))
        print(f"  {C.RED}[>>]{C.RESET} {C.BOLD}{name:<16}{C.RESET}: {C.CYAN}{link}{C.RESET}")

    print(f"\n{C.GREEN}  [✓] OSINT Recon Complete — Sabaz Ali Khan Framework{C.RESET}\n")

def menu():
    print(BANNER)
    hack_loading()
    print(f"""  {C.BOLD}{C.CYAN}  ┌─────────────[ MAIN MENU ]─────────────┐
  │  [1] Track Phone Number (Full OSINT)  │
  │  [2] Bulk Scan (file: numbers.txt)    │
  │  [0] Exit                             │
  └───────────────────────────────────────┘{C.RESET}""")
    choice = input(f"  {C.RED}{C.BOLD}root@anon~# {C.RESET}").strip()
    if choice == "1":
        num = input(f"  {C.YELLOW}[*] Enter target number (e.g. +923001234567): {C.RESET}").strip()
        analyze_number(num)
    elif choice == "2":
        try:
            with open("numbers.txt") as f:
                nums = [l.strip() for l in f if l.strip()]
        except FileNotFoundError:
            print(f"{C.RED}  [-] numbers.txt not found{C.RESET}")
            return
        for n in nums:
            analyze_number(n)
    elif choice == "0":
        typing_print(f"\n  {C.RED}>> Connection terminated. WE ARE LEGION. <<{C.RESET}\n")
        sys.exit()
    else:
        print(f"{C.RED}  [-] Invalid option{C.RESET}")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    try:
        while True:
            menu()
            input(f"  {C.DIM}[Press Enter to return to menu...]{C.RESET}")
            os.system("cls" if os.name == "nt" else "clear")
    except KeyboardInterrupt:
        print(f"\n  {C.RED}>> Ctrl+C Detected :: Exiting... WE ARE ANONYMOUS <<{C.RESET}")
        sys.exit()
