#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════╗
║   WHATSAPP OSINT Tools                 ║
╚══════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from datetime import datetime

# ─────────── COLORS ───────────
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
C = "\033[1;36m"
W = "\033[1;37m"
B = "\033[1;34m"
M = "\033[1;35m"
RESET = "\033[0m"

BANNER = f"""{R}
 ██████╗ ██╗   ██╗██████╗
██╔═══██╗██║   ██║██╔══██╗
██║   ██║██║   ██║██████╔╝
██║▄▄ ██║██║   ██║██╔══██╗
╚██████╔╝╚██████╔╝██████╔╝
 ╚══▀▀═╝  ╚═════╝ ╚═════╝ {G}
██╗    ██╗ █████╗  ██████╗███████╗██████╗ ██████╗ ██████╗ ██╗  ██╗████████╗
██║    ██║██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝╚══██╔══╝
██║ █╗ ██║███████║██║     █████╗  ██████╔╝██████╔╝██████╔╝█████╔╝    ██║
██║███╗██║██╔══██║██║     ██╔══╝  ██╔══██╗██╔═══╝ ██╔══██╗██╔═██╗    ██║
╚███╔███╔╝██║  ██║╚██████╗███████╗██║  ██║██║     ██║  ██║██║  ██╗   ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝{Y}
              ╔══════════════════════════════════════════╗{C}
              ║   [+] WHATSAPP OSINT Tools v1.0          ║
              ║   [+] Coded by: Cyber Security Engineer  ║
              ║   [+] Mr Sabaz Ali Khan                  ║
              ║   [+] Github  : whoami592 | ANONYMOUS    ║
              ╚══════════════════════════════════════════╝{RESET}
"""

def slow_print(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear():
    os.system("clear" if os.name == "posix" else "cls")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}

# ─────────── MODULE 1 : NUMBER VALIDATION + INFO ───────────
def number_info(number):
    print(f"\n{C}[═] NUMBER INTEL{RESET}")
    try:
        num = phonenumbers.parse(number)
        if not phonenumbers.is_valid_number(num):
            print(f"{R}[-] Invalid number!{RESET}")
            return None
        print(f"{G}[+] Valid Number      : {W}{num.national_number}{RESET}")
        print(f"{G}[+] Country Code      : {W}+{num.country_code}{RESET}")
        print(f"{G}[+] Country / Region  : {W}{geocoder.description_for_number(num, 'en')}{RESET}")
        print(f"{G}[+] Timezone          : {W}{', '.join(timezone.time_zones_for_number(num))}{RESET}")
        print(f"{G}[+] Carrier / Operator: {W}{carrier.name_for_number(num, 'en')}{RESET}")
        print(f"{G}[+] Number Type       : {W}{phonenumbers.number_type(num)}{RESET}")
        return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164).replace("+", "")
    except Exception as e:
        print(f"{R}[-] Parse error: {e}{RESET}")
        return None

# ─────────── MODULE 2 : WHATSAPP EXISTENCE CHECK ───────────
def wa_check(full_number):
    print(f"\n{C}[═] WHATSAPP EXISTENCE CHECK{RESET}")
    url = f"https://wa.me/{full_number}"
    try:
        r = requests.get(url, headers=UA, timeout=10, allow_redirects=True)
        # wa.me returns page content if registered; error text if not
        if r.status_code == 200 and "Looking for this number?" not in r.text:
            print(f"{G}[+] This number is REGISTERED on WhatsApp{RESET}")
            return True
        elif r.status_code == 404 or "Looking for this number" in r.text:
            print(f"{R}[-] This number is NOT on WhatsApp{RESET}")
        else:
            print(f"{Y}[!] Status {r.status_code} — inconclusive{RESET}")
    except Exception as e:
        print(f"{R}[-] Request failed: {e}{RESET}")
    return False

# ─────────── MODULE 3 : PROFILE PICTURE (AVATAR) FETCH ───────────
def avatar_check(full_number):
    print(f"\n{C}[═] PROFILE AVATAR PROBE{RESET}")
    urls = [
        f"https://api.whatsapp.com/send?phone={full_number}",
    ]
    for u in urls:
        try:
            r = requests.get(u, headers=UA, timeout=10)
            print(f"{G}[+] Probe endpoint  : {W}{u}{RESET}")
            print(f"{G}[+] HTTP Status     : {W}{r.status_code}{RESET}")
            if "business" in r.text.lower():
                print(f"{G}[+] Business Account detected: YES{RESET}")
        except Exception as e:
            print(f"{R}[-] {e}{RESET}")
    print(f"{Y}[i] DP only fetchable via WhatsApp Web session (see Deep Scan){RESET}")

# ─────────── MODULE 4 : OSINT LINK GENERATOR ───────────
def link_gen(full_number):
    print(f"\n{C}[═] OSINT LINK HUB{RESET}")
    links = {
        "wa.me Direct Chat"  : f"https://wa.me/{full_number}",
        "WhatsApp API Link"  : f"https://api.whatsapp.com/send?phone={full_number}",
        "Google Search"      : f"https://www.google.com/search?q=%22{full_number}%22",
        "Google (wa.me)"     : f"https://www.google.com/search?q=%22wa.me%2F{full_number}%22",
        "HaveIBeenPwned"     : f"https://haveibeenpwned.com/unifiedsearch/{full_number}",
        "Truecaller Search"  : f"https://www.truecaller.com/search/global/{full_number}",
        "Telegram Check"     : f"https://t.me/+{full_number}",
        "Facebook Search"    : f"https://www.facebook.com/search/top?q={full_number}",
        "Instagram Search"   : f"https://www.instagram.com/explore/search/keyword/?q={full_number}",
        "Sync.me"            : f"https://sync.me/search/?number={full_number}",
        "Eyecon"             : f"https://eyecon.online/search/{full_number}",
    }
    for name, link in links.items():
        print(f"{G}[+] {W}{name:<20} {Y}{link}{RESET}")

# ─────────── MODULE 5 : QR GENERATOR ───────────
def qr_gen(full_number):
    print(f"\n{C}[═] CLICK-TO-CHAT QR CODE{RESET}")
    try:
        import qrcode
        img = qrcode.make(f"https://wa.me/{full_number}")
        fname = f"wa_qr_{full_number}.png"
        img.save(fname)
        print(f"{G}[+] QR saved: {W}{fname}{RESET}")
    except ImportError:
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://wa.me/{full_number}"
        print(f"{Y}[i] pip install qrcode  (ya) online QR use karo:{RESET}")
        print(f"{W}{qr_url}{RESET}")

# ─────────── MODULE 6 : DEEP SCAN (WA WEB SESSION - OPTIONAL) ───────────
def deep_scan():
    print(f"\n{C}[═] DEEP SCAN INFO{RESET}")
    print(f"{Y}[i] Profile DP / About / Last-seen sirf authenticated")
    print(f"    WhatsApp Web session se nikalta hai. Steps:{RESET}")
    print(f"{W}  1. pip install selenium webdriver-manager")
    print(f"  2. web.whatsapp.com par QR scan karo (apna account)")
    print(f"  3. chat open karke DP, about, last seen scrape karo")
    print(f"  4. ya WhatsApp Business Cloud API (official) use karo{RESET}")

# ─────────── MODULE 7 : REPORT ───────────
def report(full_number, registered):
    fname = f"report_{full_number}_{random.randint(100,999)}.txt"
    with open(fname, "w") as f:
        f.write("WHATSAPP OSINT FRAMEWORK - REPORT\n")
        f.write("Coded by Cyber Security Engineer Mr Sabaz Ali Khan\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Target : +{full_number}\n")
        f.write(f"WhatsApp Registered: {registered}\n")
    print(f"{G}[+] Report saved: {W}{fname}{RESET}")

# ─────────── MAIN MENU ───────────
def main():
    clear()
    slow_print(BANNER, 0.0008)
    print(f"{M}       ┌──────────────────────────────────────┐")
    print(f"       │ 1. Number Info + Validation          │")
    print(f"       │ 2. WhatsApp Existence Check          │")
    print(f"       │ 3. Full Scan (1+2+3+4+5+Report)      │")
    print(f"       │ 4. OSINT Link Hub Only               │")
    print(f"       │ 5. QR Generator Only                 │")
    print(f"       │ 6. Deep Scan Guide                   │")
    print(f"       │ 0. Exit                              │")
    print(f"       └──────────────────────────────────────┘{RESET}")
    ch = input(f"{R}  ════> MR-TX@SABAZ:~$ {RESET}")
    if ch in ("1", "3"):
        number = input(f"{Y}[?] Enter number (with country code, e.g +92300xxxxxxx): {RESET}")
        fn = number_info(number)
        if fn is None:
            return
        if ch == "3":
            reg = wa_check(fn)
            avatar_check(fn)
            link_gen(fn)
            qr_gen(fn)
            report(fn, reg)
        input(f"{Y}[*] Enter to continue...{RESET}")
        main()
    elif ch in ("2", "4", "5"):
        number = input(f"{Y}[?] Enter number: {RESET}")
        fn = phonenumbers.parse(number)
        fn = phonenumbers.format_number(fn, phonenumbers.PhoneNumberFormat.E164).replace("+", "")
        if ch == "2": wa_check(fn)
        if ch == "4": link_gen(fn)
        if ch == "5": qr_gen(fn)
        input(f"{Y}[*] Enter to continue...{RESET}")
        main()
    elif ch == "6":
        deep_scan()
        input(f"{Y}[*] Enter to continue...{RESET}")
        main()
    elif ch == "0":
        print(f"{R}[!] Exiting... - Mr Sabaz Ali Khan | MR-TX{RESET}")
        sys.exit()
    else:
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Ctrl+D detected... Exiting{RESET}")
        sys.exit()
