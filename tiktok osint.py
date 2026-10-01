#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
    ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
       ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝
      ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗
      ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
      ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
              OSINT FRAMEWORK v1.0
"""

import os
import re
import sys
import json
import time
import random
import string
import requests
from datetime import datetime

# ================= CONFIG =================
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
TIMEOUT = 15

# ================= COLORS =================
class C:
    R = "\033[1;31m"
    G = "\033[1;32m"
    Y = "\033[1;33m"
    B = "\033[1;34m"
    M = "\033[1;35m"
    CY = "\033[1;36m"
    W = "\033[1;97m"
    END = "\033[0m"

BANNER = f"""{C.R}
 ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
 ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
    ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{C.CY}╔══════════════════════════════════════════════════════╗
║   [+]  TIKTOK OSINT FRAMEWORK  v1.0                  ║
║   [+]  TIKTOK Tracking | Username Enumeration     ║
║   [+]  Profile Recon | Media & Download Intelligence ║
║   [+]  Multi-Module Recon Engine                     ║
╠══════════════════════════════════════════════════════╣
║  Coded by Cyber Security Engineer MR SABAZ ALI KHAN  ║
║  Github : whoami592 | Team : Anonymous Hackers  ║
╚══════════════════════════════════════════════════════╝{C.END}
"""

def slow_print(text, delay=0.005):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def loading(msg="Initializing Recon Modules"):
    spin = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for _ in range(20):
        print(f"\r{C.Y}[{spin[_ % len(spin)]}] {msg}...{C.END}", end="")
        time.sleep(0.05)
    print(f"\r{C.G}[+] {msg}... DONE        {C.END}")

# ================= MODULES =================

def module_profile(username):
    """Profile info fetch - TikTok oembed (no API key required)"""
    print(f"\n{C.CY}[*] MODULE 01 :: PROFILE RECON{C.END}")
    url = f"https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{username}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200:
            d = r.json()
            data = {
                "Username": d.get("author_unique_id"),
                "Display Name": d.get("author_name"),
                "Profile Pic": d.get("thumbnail_url"),
                "Video Title": d.get("title"),
            }
            print(f"{C.G}[+] PROFILE FOUND ✅{C.END}")
            for k, v in data.items():
                print(f"{C.W}    {k:<14}: {v}{C.END}")
            return data
        else:
            print(f"{C.R}[-] Profile not reachable (HTTP {r.status_code}){C.END}")
    except Exception as e:
        print(f"{C.R}[!] Error: {e}{C.END}")
    return None

def module_existence(username):
    """Check username existence via HTTP status"""
    print(f"\n{C.CY}[*] MODULE 02 :: USERNAME EXISTENCE CHECK{C.END}")
    url = f"https://www.tiktok.com/@{username}"
    try:
        r = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code == 200:
            print(f"{C.G}[+] @{username} EXISTS on TikTok{C.END}")
            return True
        elif r.status_code == 404:
            print(f"{C.R}[-] @{username} NOT FOUND (404){C.END}")
        else:
            print(f"{C.Y}[?] HTTP {r.status_code} — likely bot-protection/JS challenge{C.END}")
    except Exception as e:
        print(f"{C.R}[!] Error: {e}{C.END}")
    return False

def module_avatar_download(username):
    """Download profile avatar"""
    print(f"\n{C.CY}[*] MODULE 03 :: AVATAR DOWNLOADER{C.END}")
    url = f"https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{username}"
    try:
        d = requests.get(url, headers=HEADERS, timeout=TIMEOUT).json()
        av = d.get("thumbnail_url")
        if av:
            fn = f"{username}_avatar.jpg"
            img = requests.get(av, headers=HEADERS, timeout=TIMEOUT).content
            with open(fn, "wb") as f:
                f.write(img)
            print(f"{C.G}[+] Avatar saved: {os.path.abspath(fn)}{C.END}")
            return fn
    except Exception as e:
        print(f"{C.R}[!] Error: {e}{C.END}")
    return None

def module_crosscheck(username):
    """Cross-check same username on other platforms"""
    print(f"\n{C.CY}[*] MODULE 04 :: CROSS-PLATFORM USERNAME RECON{C.END}")
    sites = {
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter/X": f"https://x.com/{username}",
        "GitHub":    f"https://github.com/{username}",
        "Reddit":    f"https://www.reddit.com/user/{username}",
        "Telegram":  f"https://t.me/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
    }
    for name, url in sites.items():
        try:
            r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=False)
            if r.status_code in (200,):
                print(f"{C.G}    [+] {name:<11}: FOUND   {url}{C.END}")
            elif r.status_code in (404, 301, 302):
                print(f"{C.R}    [-] {name:<11}: NOT FOUND{C.END}")
            else:
                print(f"{C.Y}    [?] {name:<11}: HTTP {r.status_code} (restricted){C.END}")
        except Exception:
            print(f"{C.Y}    [?] {name:<11}: TIMEOUT/BLOCKED{C.END}")

def module_gdork(username):
    """Generate Google dorks for deep recon"""
    print(f"\n{C.CY}[*] MODULE 05 :: GOOGLE DORK GENERATOR{C.END}")
    dorks = [
        f'site:tiktok.com "@{username}"',
        f'site:tiktok.com "{username}"',
        f'"{username}" tiktok profile',
        f'site:tiktok.com/@{username}',
        f'"@{username}" (email OR phone OR contact)',
        f'"{username}" site:linktr.ee OR site:beacons.ai',
    ]
    for d in dorks:
        print(f"{C.M}    [DORK] {d}{C.END}")
    print(f"{C.Y}    [i] Google pe paste karein ya browser mein: https://google.com/search?q={dorks[0].replace(' ', '+')}{C.END}")

def module_report(username, data):
    """Save JSON report"""
    print(f"\n{C.CY}[*] MODULE 06 :: REPORT GENERATOR{C.END}")
    report = {
        "tool": "TikTok OSINT Framework v1.0",
        "author": "Mr Sabaz Ali Khan (Cyber Security Engineer)",
        "target": username,
        "timestamp": datetime.now().isoformat(),
        "profile": data,
    }
    fn = f"report_{username}_{int(time.time())}.json"
    with open(fn, "w") as f:
        json.dump(report, f, indent=4)
    print(f"{C.G}[+] Report saved: {os.path.abspath(fn)}{C.END}")

# ================= MAIN =================
def main():
    clear()
    print(BANNER)
    slow_print(f"{C.G}      >>> Anonymous Hacker Style | MrSabazAliKhan <<< {C.END}", 0.01)
    loading()

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input(f"{C.Y}[?] Target TikTok Username (bina @): {C.W}").strip().lstrip("@")

    print(f"\n{C.R}[🎯] TARGET LOCKED: @{username}{C.END}")
    print(f"{C.M}{'─' * 54}{C.END}")

    data = module_profile(username)
    module_existence(username)
    module_avatar_download(username)
    module_crosscheck(username)
    module_gdork(username)
    module_report(username, data)

    print(f"\n{C.G}╔══════════════════════════════════════════╗")
    print(f"║  [✔] RECON COMPLETE — stay anonymous!    ║")
    print(f"║  TikTok OSINT Framework | Sabaz Ali Khan ║")
    print(f"╚══════════════════════════════════════════╝{C.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.R}[!] Interrupted by user. Bye! {C.END}")
