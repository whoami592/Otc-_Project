#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Black Hat Hacker Framework Toolkit
Coded by: Cyber Security Engineer Mr Sabaz Ali Khan
Matrix Style Design
"""

import os
import sys
import time
import random
import socket
import threading
import queue
import urllib.request
import urllib.error
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# ============================================================
#  COLORS
# ============================================================
G  = "\033[92m"   # Green (Matrix)
DG = "\033[32m"   # Dark Green
W  = "\033[97m"   # White
R  = "\033[91m"   # Red
Y  = "\033[93m"   # Yellow
C  = "\033[96m"   # Cyan
RS = "\033[0m"    # Reset

AUTHOR = "Cyber Security Engineer Mr Sabaz Ali Khan"

# ============================================================
#  MATRIX RAIN (Terminal Background Effect)
# ============================================================
def matrix_rain(duration=3, width=80, speed=0.03):
    """Matrix-style falling characters effect"""
    chars = "01ﾊﾋｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃ@#$%&*+=<>"
    cols = [random.choice(chars) for _ in range(width)]
    end = time.time() + duration
    print(G)
    while time.time() < end:
        line = ""
        for i in range(width):
            if random.random() < 0.04:
                cols[i] = random.choice(chars)
            line += cols[i] if random.random() < 0.7 else " "
        print(line)
        time.sleep(speed)
    print(RS, end="")

# ============================================================
#  BANNER
# ============================================================
BANNER = f"""{G}
 ██████╗ ██╗      █████╗  ██████╗██╗  ██╗    ██╗  ██╗ █████╗ ████████╗██╗  ██╗ █████╗ ███████╗██████╗
 ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝    ██║  ██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗██╔════╝██╔══██╗
 ██████╔╝██║     ███████║██║     █████╔╝     ███████║███████║   ██║   ███████║███████║█████╗  ██████╔╝
 ██╔══██╗██║     ██╔══██║██║     ██╔═██╗     ██╔══██║██╔══██║   ██║   ██╔══██║██╔══██║██╔══╝  ██╔══██╗
 ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗    ██║  ██║██║  ██║   ██║   ██║  ██║██║  ██║███████╗██║  ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{RS}
{C}╔══════════════════════════════════════════════════════════════════════╗
║            BLACK HAT HACKER — ADVANCED PENTEST FRAMEWORK             ║
║          Coded by : Cyber Security Engineer Mr Sabaz Ali Khan        ║
║          Version  : 1.0   |   Matrix Edition                         ║
╚══════════════════════════════════════════════════════════════════════╝{RS}
"""

# ============================================================
#  UTILS
# ============================================================
def matrix_print(msg, color=G, prefix="[*]"):
    print(f"{color}[{time.strftime('%H:%M:%S')}] {prefix} {msg}{RS}")

def ok(msg):    matrix_print(msg, G, "+")
def info(msg):  matrix_print(msg, C, "*")
def warn(msg):  matrix_print(msg, Y, "!")
def fail(msg):  matrix_print(msg, R, "-")

def get_target(prompt="Target >> "):
    t = input(f"{G}{prompt}{RS}").strip()
    if not t:
        fail("Target required!")
        return None
    return t

def get_int(prompt, default):
    try:
        return int(input(f"{G}{prompt}{RS}").strip() or default)
    except ValueError:
        return default

# ============================================================
#  MODULE 1 : PORT SCANNER  (multithreaded)
# ============================================================
def port_scan_worker(host, q, results, timeout):
    while not q.empty():
        port = q.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            if s.connect_ex((host, port)) == 0:
                try:
                    s.sendall(b"HEAD / HTTP/1.1\r\n\r\n")
                    banner = s.recv(1024).decode(errors="ignore").split("\n")[0].strip()
                except Exception:
                    banner = ""
                results.append((port, banner))
                ok(f"Port {W}{port}/tcp{G} OPEN  {Y}{banner}")
            s.close()
        except Exception:
            pass
        finally:
            q.task_done()

def module_port_scanner():
    info("PORT SCANNER — Multi-threaded TCP + Banner Grabbing")
    target = get_target("Target (IP/domain) >> ")
    if not target: return
    try:
        host = socket.gethostbyname(target)
        info(f"Resolved {target} -> {host}")
    except socket.gaierror:
        fail("DNS resolution failed"); return

    start = get_int("Start port [1] >> ", 1)
    end   = get_int("End port   [1000] >> ", 1000)
    threads_n = get_int("Threads    [100] >> ", 100)

    q = queue.Queue()
    for p in range(start, end + 1):
        q.put(p)
    results, threads = [], []
    for _ in range(min(threads_n, max(1, end - start + 1))):
        t = threading.Thread(target=port_scan_worker, args=(host, q, results, 1.0), daemon=True)
        t.start(); threads.append(t)
    q.join()
    info(f"Scan complete. {len(results)} open port(s) found.")

# ============================================================
#  MODULE 2 : SUBDOMAIN ENUMERATOR
# ============================================================
SUBS = ["www","mail","ftp","admin","portal","vpn","remote","dev","test","staging",
        "api","cpanel","webmail","ns1","ns2","blog","shop","app","cloud","secure",
        "git","jenkins","db","mysql","sql","backup","intranet","exchange","owa",
        "login","auth","sso","cdn","img","static","support","help","crm","erp"]

def module_subdomain_enum():
    info("SUBDOMAIN ENUMERATOR — DNS Brute Force")
    target = get_target("Domain (example.com) >> ")
    if not target: return
    found = 0
    threads = []
    lock = threading.Lock()

    def worker(sub):
        nonlocal found
        fqdn = f"{sub}.{target}"
        try:
            ip = socket.gethostbyname(fqdn)
            with lock:
                found += 1
                ok(f"{W}{fqdn}{G} -> {Y}{ip}")
        except socket.gaierror:
            pass

    for sub in SUBS:
        t = threading.Thread(target=worker, args=(sub,), daemon=True)
        t.start(); threads.append(t)
        if len(threads) >= 30:
            for t in threads: t.join()
            threads = []
    for t in threads: t.join()
    info(f"Done. {found} subdomain(s) discovered.")

# ============================================================
#  MODULE 3 : DIRECTORY / FILE FUZZER
# ============================================================
DIRS = ["admin","login","administrator","wp-admin","wp-login.php","dashboard",
        "backup","db","config","phpmyadmin","cpanel",".git",".env","robots.txt",
        "adminpanel","manager","user","api","uploads","install","setup","shell",
        "test","dev","old","bak","sql","backup.sql","dump","passwd",".htaccess"]

def module_dir_fuzzer():
    info("DIRECTORY FUZZER — Hidden Path Discovery")
    target = get_target("URL (http://target) >> ")
    if not target: return
    if not target.startswith("http"):
        target = "http://" + target
    found = 0
    for d in DIRS:
        url = f"{target}/{d}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            r = urllib.request.urlopen(req, timeout=5)
            found += 1
            ok(f"{W}{r.status}{G} {Y}{url}  [{len(r.read())} bytes]")
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                found += 1
                warn(f"{e.code} {url}  (protected — interesting!)")
        except Exception:
            pass
    info(f"Fuzz complete. {found} path(s) found.")

# ============================================================
#  MODULE 4 : ADMIN PANEL FINDER
# ============================================================
ADMIN_PATHS = ["admin","admin/login.php","administrator","adminpanel","cpanel",
               "admin/index.php","admin/admin.php","manage","manager","cms/admin",
               "wp-admin","admin/login","login/admin","admin/account.php",
               "admin/controlpanel.php","admincp","moderator","controlpanel"]

def module_admin_finder():
    info("ADMIN PANEL FINDER")
    target = get_target("URL (http://target) >> ")
    if not target: return
    if not target.startswith("http"):
        target = "http://" + target
    for p in ADMIN_PATHS:
        url = f"{target}/{p}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            r = urllib.request.urlopen(req, timeout=5)
            body = r.read().decode(errors="ignore").lower()
            if r.status == 200 and any(k in body for k in ("password","login","username","admin")):
                ok(f"POSSIBLE ADMIN PANEL -> {Y}{url}")
        except Exception:
            pass
    info("Admin scan complete.")

# ============================================================
#  MODULE 5 : BANNER GRABBER + SERVICE INFO
# ============================================================
def module_banner_grabber():
    info("BANNER GRABBER — Service Fingerprinting")
    target = get_target("Target (IP/domain) >> ")
    if not target: return
    try:
        host = socket.gethostbyname(target)
    except socket.gaierror:
        fail("DNS failed"); return
    ports = input(f"{G}Ports (comma separated) [21,22,25,80,443,3389] >> {RS}").strip()
    ports = [int(p) for p in ports.split(",")] if ports else [21,22,25,80,443,3389]
    for port in ports:
        try:
            s = socket.socket(); s.settimeout(3)
            s.connect((host, port))
            banner = s.recv(1024).decode(errors="ignore").strip()
            ok(f"Port {W}{port}{G} : {Y}{banner if banner else '(no banner — silent service)'}")
            s.close()
        except Exception as e:
            fail(f"Port {port} : {type(e).__name__}")

# ============================================================
#  MODULE 6 : WHOIS-STYLE BASIC INFO (DNS/Reverse)
# ============================================================
def module_target_info():
    info("TARGET INFO — DNS & Reverse Lookup")
    target = get_target("Target (IP/domain) >> ")
    if not target: return
    try:
        ip = socket.gethostbyname(target)
        ok(f"IP Address : {ip}")
    except socket.gaierror:
        fail("Cannot resolve"); return
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        ok(f"Reverse DNS: {host}")
    except Exception:
        warn("No reverse DNS record")
    ok(f"Hostname   : {socket.gethostname()} (local)")
    info("Tip: use `whois <domain>` and `dig any <domain>` on Kali for full recon.")

# ============================================================
#  MENU
# ============================================================
MODULES = {
    "1": ("Port Scanner (Multi-threaded + Banner Grab)", module_port_scanner),
    "2": ("Subdomain Enumerator (DNS Brute)",           module_subdomain_enum),
    "3": ("Directory / File Fuzzer",                     module_dir_fuzzer),
    "4": ("Admin Panel Finder",                          module_admin_finder),
    "5": ("Banner Grabber / Service Fingerprint",        module_banner_grabber),
    "6": ("Target Info / DNS Recon",                     module_target_info),
}

def menu():
    os.system("cls" if os.name == "nt" else "clear")
    matrix_rain(2)
    print(BANNER)
    while True:
        print(f"{G}  ┌──────────────────────────────────────────────────┐")
        print(f"  │{W}            BLACK HAT MODULES — SELECT            {G}│")
        print(f"  ├──────────────────────────────────────────────────┤{RS}")
        for k, (name, _) in MODULES.items():
            print(f"{G}  │ {W}[{k}]{G} {name:<47}{G}│{RS}")
        print(f"{G}  │ {W}[M]{G} Matrix Rain Effect (5 sec)                      {G}│")
        print(f"  │ {W}[0]{G} Exit                                            {G}│")
        print(f"  └──────────────────────────────────────────────────┘{RS}")
        choice = input(f"{G}  blackhat@matrix:~#{RS} ").strip().lower()
        if choice == "0":
            print(f"{G}\n  [*] Goodbye from {AUTHOR} ... stay in the matrix.{RS}\n")
            matrix_rain(1.5); sys.exit(0)
        elif choice == "m":
            matrix_rain(5); print(BANNER)
        elif choice in MODULES:
            print(BANNER)
            try:
                MODULES[choice][1]()
            except KeyboardInterrupt:
                fail("Interrupted by user")
            input(f"\n{Y}  [Press Enter to return to menu]{RS}")
            os.system("cls" if os.name == "nt" else "clear")
            print(BANNER)
        else:
            fail("Invalid choice!")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{R}  [!] Ctrl+C — exiting matrix...{RS}")
        sys.exit(0)
