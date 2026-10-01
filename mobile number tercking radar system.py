#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#   MOBILE NUMBER RADAR — GUI EDITION v2.0
#   Coded By: Cyber Security Engineer Mr. Sabaz Ali Khan
#   Anonymous x MIRTX Style
# ============================================================

import tkinter as tk
from tkinter import messagebox
import math, random, threading, time
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

BG        = "#000000"
RADAR_BG  = "#0a1a0a"
GREEN     = "#00ff00"
DIM_GREEN = "#003300"
RED       = "#ff2222"
CYAN      = "#00ffff"
YELLOW    = "#ffee00"

class MobileRadarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MOBILE NUMBER RADAR v2.0 — Coded By Mr. Sabaz Ali Khan")
        self.root.configure(bg=BG)
        self.root.geometry("1000x700")
        self.angle = 0
        self.sweeping = True
        self.targets = []          # blips: (angle, radius, label)
        self.build_ui()
        self.animate_sweep()

    # ---------------- UI ----------------
    def build_ui(self):
        # Title bar
        title = tk.Label(self.root, text="★ MOBILE NUMBER RADAR v2.0 ★",
                         font=("Consolas", 20, "bold"), fg=GREEN, bg=BG)
        title.pack(pady=5)
        tk.Label(self.root, text="Coded By: Cyber Security Engineer MR. SABAZ ALI KHAN | ANONYMOUS x MIRTX STYLE",
                 font=("Consolas", 10, "bold"), fg=RED, bg=BG).pack()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        # ---- Radar canvas ----
        self.canvas = tk.Canvas(frame, width=520, height=520, bg=RADAR_BG, highlightthickness=2,
                                highlightbackground=GREEN)
        self.canvas.pack(side="left", padx=5)
        self.cx, self.cy, self.R = 260, 260, 240
        self.draw_radar()

        # ---- Right panel ----
        panel = tk.Frame(frame, bg=BG)
        panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(panel, text="[ TARGET INPUT ]", font=("Consolas", 13, "bold"),
                 fg=CYAN, bg=BG).pack(anchor="w")
        self.entry = tk.Entry(panel, font=("Consolas", 13), bg="#0a0a0a", fg=GREEN,
                              insertbackground=GREEN, width=28)
        self.entry.pack(pady=5, anchor="w")
        self.entry.insert(0, "+923001234567")

        btns = tk.Frame(panel, bg=BG)
        btns.pack(anchor="w")
        tk.Button(btns, text="▶ SCAN", command=self.scan, bg=DIM_GREEN, fg=GREEN,
                  font=("Consolas", 12, "bold"), relief="ridge", bd=2).pack(side="left", padx=3)
        tk.Button(btns, text="✖ CLEAR", command=self.clear_targets, bg="#330000", fg=RED,
                  font=("Consolas", 12, "bold"), relief="ridge", bd=2).pack(side="left", padx=3)

        tk.Label(panel, text="[ RADAR CONSOLE ]", font=("Consolas", 13, "bold"),
                 fg=CYAN, bg=BG).pack(anchor="w", pady=(15, 0))
        self.log = tk.Text(panel, font=("Consolas", 10), bg="#0a0a0a", fg=GREEN,
                            height=22, width=48, insertbackground=GREEN)
        self.log.pack(fill="both", expand=True)

        tk.Label(self.root, text="⚠ FOR EDUCATIONAL / AUTHORIZED USE ONLY ⚠",
                 font=("Consolas", 10, "bold"), fg=YELLOW, bg=BG).pack(pady=3)

    def draw_radar(self):
        c, cx, cy, R = self.canvas, self.cx, self.cy, self.R
        # circles
        for r in (R, R*0.75, R*0.5, R*0.25):
            c.create_oval(cx-r, cy-r, cx+r, cy+r, outline=DIM_GREEN, width=2)
        # cross lines
        c.create_line(cx-R, cy, cx+R, cy, fill=DIM_GREEN, width=2)
        c.create_line(cx, cy-R, cx, cy+R, fill=DIM_GREEN, width=2)
        # degree labels
        for deg, (dx, dy) in [(0,(0,-1)),(45,(.7,-.7)),(90,(1,0)),(135,(.7,.7)),
                              (180,(0,1)),(225,(-.7,.7)),(270,(-1,0)),(315,(-.7,-.7))]:
            c.create_text(cx+dx*(R+18), cy+dy*(R+18), text=f"{deg}", fill=DIM_GREEN,
                          font=("Consolas", 8))
        # center dot
        c.create_oval(cx-4, cy-4, cx+4, cy+4, fill=GREEN, outline=GREEN)

    # ---------------- RADAR SWEEP ANIMATION ----------------
    def animate_sweep(self):
        if not self.sweeping:
            self.root.after(50, self.animate_sweep)
            return
        self.canvas.delete("sweep")
        a = math.radians(self.angle)
        x = self.cx + self.R * math.cos(a)
        y = self.cy + self.R * math.sin(a)
        # trailing gradient (5 lines fading)
        for i in range(1, 6):
            ta = math.radians(self.angle - i*4)
            tx = self.cx + self.R * math.cos(ta)
            ty = self.cy + self.R * math.sin(ta)
            shade = ["#00ff00", "#00cc00", "#009900", "#006600", "#003300"][i-1]
            self.canvas.create_line(self.cx, self.cy, tx, ty, fill=shade, width=3, tags="sweep")
        # detected blips glow when sweep passes near their angle
        self.canvas.delete("blip")
        for (bang, brad, label) in self.targets:
            diff = (self.angle - bang) % 360
            if diff < 40:  # near sweep => bright
                bx = self.cx + brad * math.cos(math.radians(bang))
                by = self.cy + brad * math.sin(math.radians(bang))
                self.canvas.create_oval(bx-6, by-6, bx+6, by+6, fill=RED, outline=RED, tags="blip")
                self.canvas.create_text(bx, by+16, text=label, fill=YELLOW,
                                        font=("Consolas", 7), tags="blip")
        self.angle = (self.angle + 3) % 360
        self.root.after(30, self.animate_sweep)

    # ---------------- SCANNING ----------------
    def log_print(self, msg, color=GREEN):
        self.log.configure(state="normal")
        self.log.insert("end", f"{msg}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def scan(self):
        number = self.entry.get().strip()
        if not number:
            messagebox.showerror("RADAR", "Mobile number dalo! (+countrycode)")
            return
        threading.Thread(target=self._scan_worker, args=(number,), daemon=True).start()

    def _scan_worker(self, number):
        self.log_print(f"[*] RADAR LOCK INIT => {number}", CYAN)
        for step in ["FREQ SYNC", "SIGNAL TRACE", "CARRIER PROBE", "GEO TRIANGULATE"]:
            self.log_print(f"    ... {step}")
            time.sleep(0.5)
        try:
            parsed = phonenumbers.parse(number, None)
        except Exception as e:
            self.log_print(f"[-] PARSE ERROR: {e}", RED)
            return
        if not phonenumbers.is_valid_number(parsed):
            self.log_print("[-] TARGET INVALID — LOCK FAILED!", RED)
            return
        operator  = carrier.name_for_number(parsed, "en") or "UNKNOWN"
        location  = geocoder.description_for_number(parsed, "en") or "UNKNOWN"
        tz        = ", ".join(timezone.time_zones_for_number(parsed)) or "UNKNOWN"
        intl      = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        region    = phonenumbers.region_code_for_number(parsed)

        self.log_print("[+] TARGET LOCKED ✔", YELLOW)
        self.log_print(f"    NUMBER   : {intl}")
        self.log_print(f"    CARRIER  : {operator}")
        self.log_print(f"    REGION   : {location} ({region})")
        self.log_print(f"    TIMEZONE : {tz}")
        self.log_print("=" * 45, DIM_GREEN)

        # random radar position for the blip
        bang = random.randint(0, 359)
        brad = random.uniform(60, self.R - 30)
        label = intl[-7:]
        self.targets.append((bang, brad, label))

    def clear_targets(self):
        self.targets.clear()
        self.canvas.delete("blip")
        self.log_print("[*] RADAR CLEARED.", CYAN)

if __name__ == "__main__":
    root = tk.Tk()
    app = MobileRadarGUI(root)
    root.mainloop()
