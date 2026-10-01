#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  ____  _____    _    ____  ___ _   _ _____ _____ ____
 |  _ \|  ___|  / \  |  _ \|_ _| \ | | ____| ____|  _ \
 | | | | |_    / _ \ | |_) || ||  \| |  _| |  _| | |_) |
 | |_| |  _|  / ___ \|  _ < | || |\  | |___| |___|  _ <
 |____/|_|   /_/   \_\_| \_\___|_| \_|_____|_____|_| \_\
 
        FACEBOOK OSINT FRAMEWORK v1.0
   Coded by Cyber Security Engineer Mr Sabaz Ali Khan
============================================================
"""

import os
import re
import sys
import time
import json
import random
import socket
import string
import requests
from datetime import datetime

# ---------------- CONFIG ----------------
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
TIMEOUT = 10
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = f"""{GREEN}{BOLD}
  ____  _____    _    ____  ___ _   _ _____ _____ ____
 |  _ \\|  ___|  / \\  |  _ \\|_ _| \\ | | ____| ____|  _ \\
 | | | | |_    / _ \\ | |_) || ||  \\| |  _| |  _| | |_) |
 | |_| |  _|  / ___ \\|  _ < | || |\\  | |___| |___|  _ <
 |____/|_|   /_/   \\_\\_| \\_\\___|_| \\_|_____|_____|_| \\_\\{RESET}

{CYAN}{BOLD}╔══════════════════════════════════════════════════════════╗
║          FACEBOOK OSINT FRAMEWORK v1.0                   ║
║      >> Anonymous Hacker Style | Matrix Mode <<          ║
║   Coded by Cyber Security Engineer Mr Sabaz Ali Khan     ║
╚══════════════════════════════════════════════════════════╝{RESET}
"""

def typewriter(text, delay=0.02):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def matrix_effect(duration=2):
    """Matrix rain intro effect"""
    chars = string.ascii_letters + string.digits + "@#$%&"
    end_time = time.time() + duration
    try:
        cols = os.get_terminal_size().columns
    except Exception:
        cols = 80
    while time.time() < end_time:
        line = "".join(random.choice(chars) if random.random() > 0.7 else " " for _ in range(cols))
        print(GREEN + line + RESET)
        time.sleep(0.05)
    print()

def log(msg, level="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    color = {"info": CYAN, "ok": GREEN, "warn": YELLOW, "err": RED}[level]
    print(f"{WHITE}[{ts}]{RESET} {color}[{level.upper()}]{RESET} {msg}")

def save_result(filename, data):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    log(f"Result saved -> {filename}", "ok")

def session():
    s = requests.Session()
    s.headers.update(HEADERS)
    return s

# ---------------- MODULES ----------------

def module_profile_info():
    """Facebook profile basic info via mobile public page"""
    typewriter(f"{YELLOW}[*] MODULE: Profile Information Extractor{RESET}")
    target = input(f"{WHITE}[?] Enter Facebook username/profile (e.g. zuck): {RESET}").strip()
    if not target:
        log("No target given!", "err"); return
    urls = [
        f"https://mbasic.facebook.com/{target}",
        f"https://www.facebook.com/{target}",
    ]
    s = session()
    result = {"target": target, "profiles": []}
    for url in urls:
        try:
            log(f"Probing: {url}", "info")
            r = s.get(url, timeout=TIMEOUT, allow_redirects=True)
            data = {
                "url": url,
                "status_code": r.status_code,
                "final_url": r.url,
                "exists": "Page Not Found" not in r.text and r.status_code == 200,
                "title": (re.search(r"<title>(.*?)</title>", r.text, re.S).group(1).strip()
                          if re.search(r"<title>(.*?)</title>", r.text, re.S) else "N/A"),
            }
            # Try extracting likes/followers counts
            for pattern, key in [
                (r'([\d,.]+)\s*(?:people\s+)?likes this', "likes"),
                (r'([\d,.]+)\s*followers', "followers"),
                (r'([\d,.]+)\s*talking about this', "talking_about"),
            ]:
                m = re.search(pattern, r.text, re.I)
                if m:
                    data[key] = m.group(1)
            result["profiles"].append(data)
            if data["exists"]:
                log(f"Profile appears ACTIVE: {data['title']}", "ok")
            else:
                log("Profile may not exist or is restricted", "warn")
        except Exception as e:
            log(f"Error: {e}", "err")
    save_result("fb_profile_info.json", result)

def module_username_hunt():
    """Username availability across platforms + Facebook ID lookup"""
    typewriter(f"{YELLOW}[*] MODULE: Username Hunter (Cross-Platform){RESET}")
    username = input(f"{WHITE}[?] Username to hunt: {RESET}").strip()
    if not username:
        return
    platforms = {
        "Facebook": f"https://www.facebook.com/{username}",
        "Facebook (mbasic)": f"https://mbasic.facebook.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter/X": f"https://twitter.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
    }
    s = session()
    found = []
    for name, url in platforms.items():
        try:
            r = s.get(url, timeout=TIMEOUT)
            taken = r.status_code == 200
            mark = GREEN + "[FOUND]" + RESET if taken else RED + "[FREE ]" + RESET
            print(f"  {mark} {name:20s} -> {url}")
            if taken and "Facebook" in name:
                found.append(url)
        except Exception:
            print(f"  {YELLOW}[ERROR]{RESET} {name}")
        time.sleep(random.uniform(0.4, 1.2))  # rate-limit friendly
    if found:
        save_result("fb_username_hunt.json", {"username": username, "hits": found})

def module_email_recon():
    """Email pattern generation + breach-style lookup via public endpoints"""
    typewriter(f"{YELLOW}[*] MODULE: Email Pattern Recon{RESET}")
    name = input(f"{WHITE}[?] Full name (e.g. John Doe): {RESET}").strip()
    domain = input(f"{WHITE}[?] Domain (default gmail.com): {RESET}").strip() or "gmail.com"
    parts = name.lower().split()
    if not parts:
        return
    first, last = parts[0], (parts[-1] if len(parts) > 1 else "")
    patterns = {
        "first.last": f"{first}.{last}@{domain}",
        "firstlast": f"{first}{last}@{domain}",
        "first_last": f"{first}_{last}@{domain}",
        "firstlast_initial": f"{first}{last[:1] if last else ''}@{domain}",
        "first_initial_last": f"{first[0]}{last}@{domain}",
        "first_only": f"{first}@{domain}",
        "last_first": f"{last}{first}@{domain}",
    }
    print(f"\n{CYAN}[*] Generated email patterns:{RESET}")
    for style, email in patterns.items():
        print(f"  {WHITE}[{style:20s}]{RESET} {GREEN}{email}{RESET}")
    save_result("fb_email_patterns.json", {"name": name, "domain": domain, "patterns": patterns})

def module_graph_lookup():
    """Facebook numeric ID / Graph public data probe"""
    typewriter(f"{YELLOW}[*] MODULE: Facebook Graph / ID Lookup{RESET}")
    uid = input(f"{WHITE}[?] Numeric Facebook ID or username: {RESET}").strip()
    if not uid:
        return
    s = session()
    endpoints = [
        f"https://graph.facebook.com/{uid}/picture?width=9999&redirect=false",
        f"https://www.facebook.com/{uid}",
        f"https://mbasic.facebook.com/profile.php?id={uid}" if uid.isdigit() else None,
    ]
    for ep in endpoints:
        if not ep:
            continue
        try:
            r = s.get(ep, timeout=TIMEOUT)
            log(f"{ep} -> HTTP {r.status_code}")
            if "graph.facebook.com" in ep and r.status_code == 200:
                print(f"  {CYAN}Response:{RESET} {r.text[:300]}")
        except Exception as e:
            log(f"Error: {e}", "err")

def module_dns_ip():
    """DNS/IP recon for custom domains (phishing/impersonation check)"""
    typewriter(f"{YELLOW}[*] MODULE: Domain DNS & IP Recon{RESET}")
    domain = input(f"{WHITE}[?] Domain (e.g. example.com): {RESET}").strip()
    if not domain:
        return
    try:
        ip = socket.gethostbyname(domain)
        log(f"Resolved IP: {GREEN}{ip}{RESET}", "ok")
        try:
            host, aliases, _ = socket.gethostbyaddr(ip)
            log(f"Reverse DNS: {host} | Aliases: {aliases}", "ok")
        except Exception:
            log("No reverse DNS record", "warn")
        save_result("fb_dns_recon.json", {"domain": domain, "ip": ip})
    except Exception as e:
        log(f"DNS lookup failed: {e}", "err")

def module_ip_logger_link():
    """Generate an IP-logger style tracking link (for authorized phishing awareness tests)"""
    typewriter(f"{YELLOW}[*] MODULE: Tracking Link Generator (Awareness/Red Team){RESET}")
    log("This module creates a link that logs visitor IP + UA when opened.", "warn")
    webhook = input(f"{WHITE}[?] Enter your webhook/collector URL (e.g. your server endpoint): {RESET}").strip()
    if not webhook:
        log("No collector URL provided", "err"); return
    redirect_target = input(f"{WHITE}[?] Redirect target (default https://facebook.com): {RESET}").strip() or "https://facebook.com"
    # Simple encoded redirect that forwards data to collector
    import urllib.parse
    payload = urllib.parse.quote(redirect_target)
    link = f"{webhook}?redirect={payload}"
    print(f"\n{GREEN}[+] Tracking Link:{RESET} {BOLD}{link}{RESET}")
    print(f"{CYAN}[*] Victim side will hit your collector; log IP + User-Agent on your server.{RESET}")
    save_result("fb_tracking_link.json", {"link": link, "collector": webhook})

# ---------------- MENU ----------------

MODULES = {
    "1": ("Profile Information Extractor", module_profile_info),
    "2": ("Username Hunter (Cross-Platform)", module_username_hunt),
    "3": ("Email Pattern Recon", module_email_recon),
    "4": ("Facebook Graph / ID Lookup", module_graph_lookup),
    "5": ("Domain DNS & IP Recon", module_dns_ip),
    "6": ("Tracking Link Generator", module_ip_logger_link),
    "0": ("Exit", None),
}

def main_menu():
    while True:
        print(f"\n{CYAN}{BOLD}┌──[ FACEBOOK OSINT FRAMEWORK — MAIN MENU ]──────────────┐{RESET}")
        for k, (name, _) in MODULES.items():
            print(f"{GREEN}│  [{k}] {name:<50}│{RESET}")
        print(f"{CYAN}{BOLD}└────────────────────────────────────────────────────────┘{RESET}")
        choice = input(f"{WHITE}┌─[FB-OSINT]─┐ > {RESET}").strip()
        if choice == "0":
            print(f"{RED}{BOLD}[!] Shutting down... Stay Anonymous. ~ Mr Sabaz Ali Khan{RESET}")
            break
        mod = MODULES.get(choice)
        if mod and mod[1]:
            try:
                mod[1]()
            except KeyboardInterrupt:
                log("Module aborted by user", "warn")
            input(f"{YELLOW}[*] Press ENTER to return to menu...{RESET}")
        else:
            log("Invalid selection!", "err")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    matrix_effect(2)
    print(BANNER)
    typewriter(f"{GREEN}[>>] Initializing FACEBOOK OSINT FRAMEWORK ...", 0.03)
    typewriter(f"{CYAN}[>>] Coded by Cyber Security Engineer {BOLD}Mr Sabaz Ali Khan{RESET}", 0.03)
    typewriter(f"{YELLOW}[>>] Matrix Mode: ENGAGED | Stay Anonymous{RESET}", 0.03)
    print()
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Interrupted. Exiting...{RESET}")

if __name__ == "__main__":
    main()
