#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║   BlueSecure Bluetooth Security Toolkit v1.0         ║
║   Coded by Cyber Security Engineer: Sabaz Ali Khan   ║
║   For Authorized Security Testing & Education Only   ║
╚══════════════════════════════════════════════════════╝
"""

import sys
import time
import subprocess
import random
import threading

try:
    import bluetooth
except ImportError:
    print("[!] PyBluez missing. Install: pip install pybluez\n    Linux: sudo apt-get install bluez libbluetooth-dev python3-dev")
    sys.exit(1)

# ─────────────── Matrix-style Banner ───────────────
GREEN = "\033[92m"
CYAN  = "\033[96m"
RED   = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def random_char():
    return random.choice("01╬═╦╩╠╣ABCDEF10ABCDEF01")

def matrix_intro(duration=2.5):
    """Matrix rain intro animation."""
    end = time.time() + duration
    cols = 70
    while time.time() < end:
        line = "".join(random.choice("01") if random.random() > 0.5 else " "
                       for _ in range(cols))
        print(GREEN + line + RESET)
        time.sleep(0.03)
    print("\n" * 2)

BANNER = f"""{GREEN}
  ____  _              _____                        _             
 |  _ \\| |            |  ___|__  _ __ ___  ___ ___| |_ _ __ ___  
 | |_) | |   _____    | |_ / _ \\| '__/ _ \\/ __/ _ \\ __| '__/ _ \\
 |  _ <| |__|_____|   |  _| (_) | | |  __/\\__ \\  __/ |_| | | (_) |
 |_| \\_\\_____|        |_|  \\___/|_|  \\___||___/\\___|\\__|_|  \\___/
{CYAN}
 ╔═══════════════════════════════════════════════════════════╗
 ║        BlueSecure Bluetooth Security Toolkit              ║
 ║        Coded by Cyber Security Engineer                   ║
 ║        >> SABAZ ALI KHAN <<                               ║
 ║        [ Matrix Edition :: Anonymous Style ]              ║
 ╚═══════════════════════════════════════════════════════════╝{RESET}
"""

def slow_print(text, delay=0.01):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def target_prompt():
    slow_print(f"{YELLOW}[*] Initializing BlueSecure modules...{RESET}")
    time.sleep(0.3)

# ─────────────── Modules ───────────────
def bt_scan():
    print(f"{GREEN}[+]{RESET} Scanning for nearby Bluetooth devices...")
    try:
        devices = bluetooth.discover_devices(lookup_names=True, duration=8)
        if not devices:
            print(f"{RED}[-]{RESET} No devices found. Make sure Bluetooth adapter is ON (hciconfig hci0 up).")
            return
        for addr, name in devices:
            print(f"  {GREEN}[+]{RESET} {name or 'Unknown':30s} {addr}")
    except Exception as e:
        print(f"{RED}[!]{RESET} Scan error: {e}")

def sdp_enum(addr):
    print(f"{GREEN}[+]{RESET} Enumerating services on {addr}...")
    try:
        services = bluetooth.find_service(address=addr)
        if not services:
            print(f"{YELLOW}[~]{RESET} No services found.")
        for s in services:
            print(f"  Name: {s.get('name','?'):25s} Proto: {s.get('protocol','?'):8s} Port: {s.get('port','?')}")
    except Exception as e:
        print(f"{RED}[!]{RESET} SDP error: {e}")

def spp_probe(addr):
    print(f"{GREEN}[+]{RESET} Probing SPP channel (RFCOMM) on {addr}...")
    for port in range(1, 31):
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((addr, port))
            print(f"  {GREEN}[+]{RESET} OPEN RFCOMM channel {port}")
            sock.close()
        except Exception:
            pass
    print(f"{YELLOW}[~]{RESET} SPP probe complete.")

def rfcomm_ping(addr):
    print(f"{GREEN}[+]{RESET} Pinging {addr} via L2CAP...")
    cmd = ["l2ping", "-c", "4", addr]
    subprocess.call(cmd)

def info():
    print(CYAN + """
  BlueSecure Modules:
   1) Device Scan        - Discover nearby BT devices
   2) SDP Enum           - List services on target
   3) SPP/RFCOMM Probe   - Find open channels
   4) L2CAP Ping         - Connectivity check
   5) Adapter Info       - Local BT adapter status

  NOTE: Use only on devices you own or have written
  authorization to test. {RESET}""")

def adapter_info():
    print(f"{GREEN}[+]{RESET} Local Bluetooth adapter:")
    subprocess.call(["hciconfig", "-a"])

# ─────────────── Main Menu ───────────────
def main():
    matrix_intro()
    print(BANNER)
    target_prompt()
    while True:
        print(f"""
{CYAN}┌──[ BlueSecure Command Center ]──────────────┐{RESET}
│  [1] Bluetooth Device Scan                   │
│  [2] SDP Service Enumeration                 │
│  [3] RFCOMM/SPP Port Probe                   │
│  [4] L2CAP Ping (l2ping)                     │
│  [5] Local Adapter Info                      │
│  [0] Exit                                    │
{CYAN}└──────────────────────────────────────────────┘{RESET}""")
        choice = input(f"{GREEN}root@bluesecure:~#{RESET} ").strip()

        if choice == "1":
            bt_scan()
        elif choice == "2":
            t = input(f"{YELLOW}[?]{RESET} Target MAC: ").strip()
            if t: sdp_enum(t)
        elif choice == "3":
            t = input(f"{YELLOW}[?]{RESET} Target MAC: ").strip()
            if t: spp_probe(t)
        elif choice == "4":
            t = input(f"{YELLOW}[?]{RESET} Target MAC: ").strip()
            if t: rfcomm_ping(t)
        elif choice == "5":
            adapter_info()
        elif choice == "0":
            slow_print(f"{RED}[!]{RESET} Shutting down BlueSecure... Stay anonymous. Keep hacking ethically.")
            sys.exit(0)
        else:
            print(f"{RED}[-]{RESET} Invalid option!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!]{RESET} Interrupted. Exiting.")
        sys.exit(0)
