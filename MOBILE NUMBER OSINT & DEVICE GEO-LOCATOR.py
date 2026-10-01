#!/usr/bin/env python3
# ============================================================
#   MOBILE TRACKING TOOL  |  Coded by Cyber Security Engineer
#   Mr Sabaz Ali Khan  |  Anonymous + Matrix Hacker Style
# ============================================================
#  DISCLAIMER: For educational / authorized security use only.
#  Analyzes phone number metadata (public data) & IP geolocation.
# ============================================================

import os
import sys
import time
import random
import socket
import requests

try:
    from phonenumbers import geocoder, carrier, parse, is_valid_number, number_type, PhoneNumberType
except ImportError:
    print("[!] Run: pip install phonenumbers requests")
    sys.exit(1)

# ---------------- CONFIG ----------------
AUTHOR = "Coded by Cyber Security Engineer Mr Sabaz Ali Khan"
TOOL_NAME = "MOBILE TRACKING"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def matrix_rain(duration=3):
    """Anonymous style Matrix rain intro"""
    chars = "01ｱｲｳｴｵｶｷｸｹｺﾊﾋﾌﾍﾎABCDEF#$%&"
    end = time.time() + duration
    cols, _ = os.get_terminal_size() if hasattr(os, "get_terminal_size") else (80, 24)
    print(GREEN)
    while time.time() < end:
        line = "".join(random.choice(chars) if random.random() > 0.85 else " " for _ in range(cols))
        print(line)
        sys.stdout.flush()
        time.sleep(0.05)
    print(RESET)
    clear()


def banner():
    b = f"""{GREEN}{BOLD}
  ███╗   ███╗ ██████╗ ██████╗ ██╗██╗     ███████╗
  ████╗ ████║██╔═══██╗██╔══██╗██║██║     ██╔════╝
  ██╔████╔██║██║   ██║██████╔╝██║██║     █████╗
  ██║╚██╔╝██║██║   ██║██╔══██╗██║██║     ██╔══╝
  ██║ ╚═╝ ██║╚██████╔╝██║  ██║██║███████╗███████╗
  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
        ████████ ██████   ██████  ██████
           ██    ██   ██ ██    ██ ██   ██
          ██    ██████  ██    ██ ██████
         ██    ██   ██ ██    ██ ██   ██
        ██    ██   ██  ██████  ██   ██

     >> MOBILE NUMBER OSINT & DEVICE GEO-LOCATOR <<
     {CYAN}{AUTHOR}{RESET}
     {YELLOW}[+] Anonymous | Matrix Style | v1.0{RESET}
     {RED}[!] For Educational & Authorized Use Only{RESET}
"""
    for line in b.splitlines():
        print(line)
        time.sleep(0.05)


def type_out(text, color=GREEN, delay=0.02):
    print(color, end="")
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(RESET)


def trace_phone():
    num = input(f"\n{YELLOW}[?] Enter phone number with country code (e.g. +92300xxxxxxx): {RESET}").strip()
    try:
        p = parse(num, None)
    except Exception:
        print(RED + "[!] Invalid number format!" + RESET)
        return

    if not is_valid_number(p):
        print(RED + "[!] Number is not valid!" + RESET)
        return

    region = geocoder.description_for_number(p, "en")
    car = carrier.name_for_number(p, "en")
    ntype = {
        PhoneNumberType.MOBILE: "MOBILE",
        PhoneNumberType.FIXED_LINE: "FIXED LINE",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "FIXED/MOBILE",
        PhoneNumberType.VOIP: "VoIP (Internet Number)",
        PhoneNumberType.TOLL_FREE: "TOLL FREE",
    }.get(number_type(p), "OTHER/UNKNOWN")

    print(f"\n{GREEN}{BOLD}=========== TRACE REPORT ==========={RESET}")
    type_out(f" [+] Number      : {p}")
    type_out(f" [+] Valid       : YES")
    type_out(f" [+] Region      : {region or 'Unknown'}")
    type_out(f" [+] Carrier     : {car or 'Unknown'}")
    type_out(f" [+] Line Type   : {ntype}")
    type_out(f" [+] Country Code : +{p.country_code}")
    print(f"{GREEN}{BOLD}===================================={RESET}\n")


def trace_ip():
    ip = input(f"\n{YELLOW}[?] Target IP (your device / authorized asset): {RESET}").strip() or requests.get("https://api.ipify.org").text
    try:
        d = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
    except Exception as e:
        print(RED + f"[!] Lookup failed: {e}" + RESET)
        return

    print(f"\n{MAGENTA}{BOLD}=========== IP GEO REPORT ==========={RESET}")
    for k, v in d.items():
        type_out(f" [+] {k:<13}: {v}")
    print(f"{MAGENTA}{BOLD}====================================={RESET}\n")


def main():
    clear()
    matrix_rain(2)
    banner()
    while True:
        print(f"""{CYAN}
 [1] Trace Phone Number (OSINT metadata)
 [2] Trace IP Address  (Geo-locate device)
 [0] Exit / Disconnect
{RESET}""")
        ch = input(f"{YELLOW} [root@matrix]~# {RESET}").strip()
        if ch == "1":
            trace_phone()
        elif ch == "2":
            trace_ip()
        elif ch == "0":
            type_out("\n [*] Connection terminated. Stay Anonymous...", RED)
            break
        else:
            print(RED + " [!] Invalid choice!" + RESET)


if __name__ == "__main__":
    main()
