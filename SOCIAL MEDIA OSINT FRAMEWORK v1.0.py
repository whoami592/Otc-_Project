#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
   SOCIAL MEDIA OSINT FRAMEWORK
   Coded By Cyber Security Engineer Mr Sabaz Ali Khan
╚══════════════════════════════════════════════════════════╝
"""

import sys
import time
import random
import subprocess
import requests
from urllib.parse import quote

# ─────────── COLORS ───────────
class C:
    R = "\033[1;31m"; G = "\033[1;32m"; Y = "\033[1;33m"
    B = "\033[1;34m"; P = "\033[1;35m"; CY = "\033[1;36m"
    W = "\033[1;37m"; GREY = "\033[1;90m"; END = "\033[0m"

# ─────────── BANNER ───────────
BANNER = f"""{C.GREY}
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
 █{C.R} ███████╗ ██████╗ ██╗███╗   ██╗████████╗{C.GREY} █
 █{C.R} ██╔════╝██╔═══██╗██║████╗  ██║╚══██╔══╝{C.GREY} █
 █{C.R} ███████╗██║   ██║██║██╔██╗ ██║   ██║   {C.GREY} █
 █{C.R} ╚════██║██║   ██║██║██║╚██╗██║   ██║   {C.GREY} █
 █{C.R} ███████║╚██████╔╝██║██║ ╚████║   ██║   {C.GREY} █
 █{C.R} ╚══════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝   ╚═╝   {C.GREY} █
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
{C.P}   ██████╗ ███████╗██╗███╗   ██╗████████╗
   ██╔══██╗██╔════╝██║████╗  ██║╚══██╔══╝
   ██████╔╝█████╗  ██║██╔██╗ ██║   ██║
   ██╔══██╗██╔══╝  ██║██║╚██╗██║   ██║
   ██████╔╝███████╗██║██║ ╚████║   ██║
   ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝{C.GREY}
 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
{C.CY}      [ SOCIAL MEDIA OSINT FRAMEWORK v1.0 ]{C.GREY}
 ═══════════════════════════════════════════════════════════{C.G}
        Coded By Cyber Security Engineer
     ██▓▒░ Mr Sabaz Ali Khan ░▒▓██{C.GREY}
 ═══════════════════════════════════════════════════════════
{C.Y}   \"We Are Anonymous. We Are Legion. We Do Not Forgive.\"{C.GREY}
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{C.END}
"""

def slow_print(text, delay=0.02):
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush()
        time.sleep(delay)
    print()

def boot_sequence():
    lines = [
        "[*] Initializing OSINT Engine...",
        "[*] Loading module: username_recon.py",
        "[*] Loading module: social_locator.py",
        "[*] Bypassing rate limits... OK",
        "[*] Establishing encrypted tunnel... OK",
        "[+] SYSTEM ONLINE. WELCOME, OPERATOR."
    ]
    for l in lines:
        print(f"{C.G}{l}{C.END}")
        time.sleep(random.uniform(0.15, 0.4))

# ─────────── PLATFORM DATABASE ───────────
PLATFORMS = {
    "GitHub":     "https://github.com/{}",
    "Twitter/X":  "https://x.com/{}",
    "Instagram":  "https://www.instagram.com/{}",
    "Reddit":     "https://www.reddit.com/user/{}",
    "Facebook":   "https://www.facebook.com/{}",
    "TikTok":     "https://www.tiktok.com/@{}",
    "Pinterest":  "https://www.pinterest.com/{}",
    "Medium":     "https://medium.com/@{}",
    "Steam":      "https://steamcommunity.com/id/{}",
    "Telegram":   "https://t.me/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Twitch":     "https://www.twitch.tv/{}",
    "Spotify":    "https://open.spotify.com/user/{}",
    "LinkedIn":   "https://www.linkedin.com/in/{}",
    "YouTube":    "https://www.youtube.com/@{}",
    "GitLab":     "https://gitlab.com/{}",
    "Behance":    "https://www.behance.net/{}",
    "Gravatar":   "https://en.gravatar.com/{}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0"
}

def check_platform(name, url, proxy=None):
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        r = requests.get(url, headers=HEADERS, timeout=8,
                         allow_redirects=False, proxies=proxies)
        if r.status_code == 200:
            return "FOUND", C.G
        elif r.status_code in (301, 302) and name == "Facebook":
            return "FOUND", C.G
        elif r.status_code == 404:
            return "NOT FOUND", C.R
        elif r.status_code == 403:
            return "BLOCKED/RESTRICTED", C.Y
        return f"HTTP {r.status_code}", C.Y
    except requests.exceptions.Timeout:
        return "TIMEOUT", C.Y
    except requests.exceptions.RequestException:
        return "ERROR", C.R

def username_hunt(username, proxy=None):
    print(f"\n{C.CY}[*] Target: {C.W}{username}{C.END}")
    print(f"{C.CY}[*] Scanning {len(PLATFORMS)} platforms...\n{C.END}")
    found = 0
    for name, url in PLATFORMS.items():
        status, color = check_platform(name, url.format(quote(username)), proxy)
        icon = "✔" if status == "FOUND" else "✘" if status == "NOT FOUND" else "?"
        print(f"  {C.GREY}[{icon}]{C.END} {C.W}{name:<12}{C.END} → {color}{status}{C.END}")
        if status == "FOUND":
            found += 1
            print(f"      {C.G}└─→ {url.format(username)}{C.END}")
    print(f"\n{C.G}[+] Recon complete: {C.W}{found}{C.G} profile(s) discovered out of {len(PLATFORMS)}{C.END}\n")
    return found

def google_dorks(username):
    print(f"\n{C.CY}[*] Generating Google Dork Queries for: {C.W}{username}{C.END}\n")
    dorks = {
        "All Social Profiles": f'"{username}" (site:instagram.com OR site:twitter.com OR site:facebook.com OR site:linkedin.com)',
        "Leaked Credentials":  f'"{username}" (password OR passwd OR pwd) filetype:txt',
        "Email Exposure":      f'"{username}" (@gmail.com OR @yahoo.com OR @outlook.com)',
        "Documents/Files":     f'"{username}" (filetype:pdf OR filetype:doc OR filetype:xls)',
        "Paste Sites":         f'"{username}" (site:pastebin.com OR site:ghostbin.com)',
        "Phone Number":        f'"{username}" (intext:"phone" OR intext:"mobile")',
    }
    for name, dork in dorks.items():
        print(f"  {C.Y}[DORK]{C.END} {C.W}{name}{C.END}")
        print(f"  {C.GREY}└─→ https://www.google.com/search?q={quote(dork)}{C.END}\n")

def open_in_firefox(url):
    try:
        subprocess.Popen(["firefox", url])
        print(f"{C.G}[+] Launched in Firefox{C.END}")
    except FileNotFoundError:
        print(f"{C.R}[-] Firefox not found{C.END}")

# ─────────── MAIN MENU ───────────
def menu():
    while True:
        print(f"""{C.P}
  ┌─────────────────────────────────────────────┐
  │{C.W}          OSINT FRAMEWORK — MENU             {C.P}│
  ├─────────────────────────────────────────────┤
  │{C.G}  [1]{C.W} Username Hunt (Social Media Scan)    {C.P}│
  │{C.G}  [2]{C.W} Google Dork Generator                {C.P}│
  │{C.G}  [3]{C.W} Open Profile URL in Firefox          {C.P}│
  │{C.G}  [4]{C.W} About / Credits                      {C.P}│
  │{C.R}  [0]{C.W} Exit                                 {C.P}│
  └─────────────────────────────────────────────┘{C.END}""")
        try:
            ch = input(f"{C.CY}  root@sabaz-osint:~# {C.END}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.R}[-] Connection terminated. Goodbye, operator.{C.END}")
            sys.exit(0)

        if ch == "1":
            u = input(f"{C.CY}  Enter target username: {C.END}").strip()
            p = input(f"{C.GREY}  Proxy (optional, e.g. http://127.0.0.1:8080): {C.END}").strip()
            username_hunt(u, p or None)
        elif ch == "2":
            u = input(f"{C.CY}  Enter target username: {C.END}").strip()
            google_dorks(u)
        elif ch == "3":
            u = input(f"{C.CY}  Profile URL: {C.END}").strip()
            open_in_firefox(u)
        elif ch == "4":
            print(f"""{C.Y}
  ═══════════════════════════════════════════
   SOCIAL MEDIA OSINT FRAMEWORK v1.0
   Coded By Cyber Security Engineer
   Mr Sabaz Ali Khan
   "We Are Anonymous. We Are Legion."
  ═══════════════════════════════════════════{C.END}""")
        elif ch == "0":
            slow_print(f"{C.R}[*] Shutting down OSINT engine... Stay anonymous.{C.END}")
            sys.exit(0)
        else:
            print(f"{C.R}[-] Invalid choice{C.END}")

if __name__ == "__main__":
    try:
        print(BANNER)
        boot_sequence()
        menu()
    except KeyboardInterrupt:
        print(f"\n{C.R}[-] Interrupted. Stay safe, operator.{C.END}")
        sys.exit(0)
