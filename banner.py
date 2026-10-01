#!/usr/bin/env python3
"""
DANGER BANNER - Matrix x Anonymous x Dragon style Coded By Mr Sabaz ali khan
Run: python3 danger_banner.py
"""

import os
import random
import sys
import time

# ---------- COLORS ----------
GREEN = "\033[38;5;46m"
DARK_GREEN = "\033[38;5;22m"
RED = "\033[38;5;196m"
WHITE = "\033[97m"
GREY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

DRAGON = r"""
             /   \       //\\        |\___/|  Coded By Cyber Security Engineer Mr Sabaz ali khan    
            | /\ |      ( .. )      /  o o  \
        ____| \/ |____   \ == /     \  ~ / __
       / == |    | == \  | vv |       \/=\/  \
       \===/|    |\===/  / /\ \        \  /  /
        \  /|    |\  /  / /  \ \      /  \  /
         \/ |    | \/  / /    \ \    (    )/
            |____|      ///  ||  \\    \  /
           /      \    ((    ||    ))  /  /
           \      /     \\__/||\__//  |  |
            \____/       \___/||\___/  |  |
        \_____________________/  \________/
"""

HACKER_MASK = r"""
     .-"      "-.  Coded Cyber Security engineer Mr sabaz ali khan 
    /            \
   |   .--.  .--. |
   |  /    \/    \|
   | |  O || O |  |
   |  \  .--.  /  |
   |   \ \__/ /   |
    \   \_/\_/   /
     '-.______.-'
"""

BANNER = r"""
 ██████╗  █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗
 ██╔══██╗██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
 ██║  ██║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
 ██║  ██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
 ██████╔╝██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def typing(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def hex_dump_filler(width=70, lines=3):
    """Fake hex dump for extra hacker style"""
    for _ in range(lines):
        row = " ".join(f"{random.randint(0,255):02x}" for _ in range(12))
        print(f"{GREY}  0x{random.randint(0x1000,0xFFFF):04x}: {row}{RESET}")


def matrix_rain(duration=3, width=60, fps=0.08):
    """Classic matrix rain animation"""
    columns = [0] * width
    end = time.time() + duration
    chars = "01ｱｲｳｴｵｶｷｸ ABCDEF#$%&"
    while time.time() < end:
        print("\033[H", end="")  # move cursor home
        for i in range(width):
            head = random.choice(chars)
            tail = random.choice(chars)
            columns[i] = max(0, columns[i] - random.randint(0, 3))
            if columns[i] == 0:
                columns[i] = random.randint(2, 10)
        frame = ""
        for row in range(20):
            for col in range(width):
                if (columns[col] + row) % 7 == 0:
                    frame += GREEN + random.choice(chars) + RESET
                else:
                    frame += " "
            frame += "\n"
        print(frame)
        time.sleep(fps)


def show_banner():
    clear()
    print(BOLD + GREEN)
    print(DRAGON)
    print(RESET)
    hex_dump_filler(70, 2)
    print()
    print(RED + BOLD + BANNER + RESET)
    print()
    print(GREEN + BOLD + HACKER_MASK + RESET)
    typing("  [!] SYSTEM BREACH DETECTED — DANGER PROTOCOL ENGAGED", 0.03)
    typing("  [!] WE ARE LEGION. WE DO NOT FORGIVE. EXPECT US.", 0.03)
    hex_dump_filler(70, 2)
    print()
    input(WHITE + "  [Press ENTER to launch matrix rain...]" + RESET)
    matrix_rain(duration=4)


if __name__ == "__main__":
    try:
        show_banner()
    except KeyboardInterrupt:
        print(RESET + "\n[!] Aborted.")
        sys.exit(0)
