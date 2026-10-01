#!/usr/bin/env python3
# ============================================
#  MobileIMEI Tracker - Security Recon Tool
#  Coded by: Cyber Security Engineer
#  Mr. Sabaz Ali Khan
# ============================================

import os
import sys
import time
import random
import subprocess

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def luhn_check(imei):
    """IMEI Luhn checksum validation"""
    if len(imei) != 15 or not imei.isdigit():
        return False
    total = 0
    for i, d in enumerate(imei):
        n = int(d)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def matrix_banner():
    green = "\033[92m"
    reset = "\033[0m"
    clear()
    banner = f"""{green}
  ██╗  ██╗ █████╗  ██████╗██╗  ██╗
  ██║ ██╔╝██╔══██╗██╔════╝██║ ██╔╝
  █████╔╝ ███████║██║     █████╔╝
  ██╔═██╗ ██╔══██║██║     ██╔═██╗
  ██║  ██╗██║  ██║╚██████╗██║  ██╗
  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
         I M E I   T R A C K E R
{reset}"""
    print(banner)
    print(f"""{green}
  ╔══════════════════════════════════════════╗
  ║      [ Mobile IMEI Tracker v1.0 ]        ║
  ║   Coded by: Mr. Sabaz Ali Khan           ║
  ║   Cyber Security Engineer                ║
  ║   only for ethical and educational use   ║
  ╚══════════════════════════════════════════╝
{reset}""")

def matrix_rain(duration=3):
    """Matrix falling code animation"""
    green = "\033[92m"
    reset = "\033[0m"
    chars = "01ABCDEFimeitracker<>{}[]#$%&*"
    cols, _ = subprocess.run(["stty", "size"] if os.name != "nt" else ["mode", "con"],
                             capture_output=True, text=True).stdout.split() if os.name != "nt" else (80, 24)
    end = time.time() + duration
    while time.time() < end:
        line = "".join(random.choice(chars) if random.random() > 0.7 else " "
                       for _ in range(80))
        print(f"{green}{line}{reset}")
        time.sleep(0.05)

def imei_info(imei):
    """TAC database se device info nikalta hai (public API)"""
    import urllib.request, json
    try:
        url = f"https://api.imei.info/v1/luhn-check?imei={imei}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def main():
    matrix_banner()
    matrix_rain(2)
    while True:
        print(f"\n\033[92m[+]\033[0m IMEI daalo (15 digit) ya 'exit': ", end="")
        imei = input().strip()
        if imei.lower() in ("exit", "quit", "q"):
            print("\n[+] Sabaz Ali Khan - Signing off... Jai Hind\n")
            sys.exit(0)
        print("\n[*] Validating IMEI (Luhn Algorithm)...")
        time.sleep(1)
        if luhn_check(imei):
            print(f"\033[92m[✓] IMEI {imei} VALID hai!\033[0m")
            print("[*] TAC database se device info fetch kar rahe hain...")
            info = imei_info(imei)
            for k, v in info.items():
                print(f"    {k}: {v}")
        else:
            print("\033[91m[✗] INVALID IMEI - Luhn check fail!\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Exiting...")
        sys.exit(0)
