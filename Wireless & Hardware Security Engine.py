#!/usr/bin/env python3
"""
================================================================================
  SignalScope & Cellular Monitor - Wireless & Hardware Security Engine
  Coded by Mr. Sabaz Ali Khan
  
  Architecture: Real-Time Spectrum Analysis, RF Signal Monitoring & IMSI Anomaly Detection
================================================================================
"""

import math
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


# ==============================================================================
# DATA STRUCTURES & DATA CLASSES
# ==============================================================================

@dataclass
class CellTower:
    cell_id: int
    mcc: int  # Mobile Country Code
    mnc: int  # Mobile Network Code
    lac: int  # Location Area Code
    frequency_mhz: float
    signal_power_dbm: float
    ta: int   # Timing Advance (Distance metric)
    encrypted: bool
    is_suspicious: bool = False
    flag_reason: str = ""


@dataclass
class RFScanPoint:
    frequency_mhz: float
    power_dbm: float
    noise_floor_dbm: float
    snr_db: float


# ==============================================================================
# CORE ENGINE: SIGNAL MONITOR & ANOMALY DETECTOR
# ==============================================================================

class SignalScopeEngine:
    """
    Core Wireless Security Engine designed by Mr. Sabaz Ali Khan.
    Provides signal spectrum visualization, IMSI catcher detection, and cellular monitoring.
    """

    def __init__(self, interface: str = "sdr0"):
        self.interface = interface
        self.developer = "Mr. Sabaz Ali Khan"
        self.baseline_towers: Dict[int, CellTower] = {}
        self.log_history: List[str] = []

    def log(self, message: str, level: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        formatted_log = f"[{timestamp}] [{level}] {message}"
        self.log_history.append(formatted_log)
        print(formatted_log)

    def scan_rf_spectrum(self, start_freq_mhz: float, stop_freq_mhz: float, step_mhz: float = 0.5) -> List[RFScanPoint]:
        """
        Simulates RF Spectrum Sweep across specified frequency range (e.g., GSM 900 / LTE 1800).
        Calculates SNR and identifies elevated power levels.
        """
        scan_results = []
        current_freq = start_freq_mhz
        noise_floor = -105.0  # Standard thermal noise floor in dBm

        while current_freq <= stop_freq_mhz:
            # Generate baseline signal with occasional peak spikes (active channels)
            is_active_channel = (abs(current_freq - 935.2) < 0.2) or (abs(current_freq - 948.6) < 0.2)
            if is_active_channel:
                power = random.uniform(-65.0, -45.0)
            else:
                power = noise_floor + random.uniform(0.0, 8.0)

            snr = power - noise_floor
            scan_results.append(RFScanPoint(
                frequency_mhz=round(current_freq, 2),
                power_dbm=round(power, 2),
                noise_floor_dbm=noise_floor,
                snr_db=round(snr, 2)
            ))
            current_freq += step_mhz

        return scan_results

    def render_ascii_spectrum(self, scan_points: List[RFScanPoint]) -> None:
        """
        Displays ASCII-based Waterfall/Spectrum graph for fast visual analysis in terminal.
        """
        print("\n" + "=" * 70)
        print(" [SignalScope] RF Spectrum Graph (Frequency vs Power dBm)")
        print(" Coded by: " + self.developer)
        print("=" * 70)

        for point in scan_points[::2]:  # Downsample for ASCII rendering width
            # Map dBm range (-110 to -40) to 30 visual bar characters
            norm_power = max(0, min(30, int((point.power_dbm + 110) * (30 / 70))))
            bar = "█" * norm_power
            indicator = "<-- HIGH POWER CHANNEL" if point.power_dbm > -60.0 else ""
            print(f"{point.frequency_mhz:6.1f} MHz | {point.power_dbm:6.1f} dBm | {bar:<30} {indicator}")
        
        print("=" * 70 + "\n")

    def analyze_cellular_towers(self, detected_towers: List[CellTower]) -> List[CellTower]:
        """
        Advanced Cellular Anomaly Detection Engine.
        Identifies rogue base stations (IMSI Catchers / StingRays) via heuristic rules:
        1. Encryption downgrades (A5/0 or Null cipher enforcement).
        2. Unnaturally high signal strength combined with LAC changes.
        3. Zero Timing Advance (TA) anomalies.
        """
        self.log(f"Analyzing {len(detected_towers)} detected cell towers...")
        processed_towers = []

        for tower in detected_towers:
            suspicious = False
            reasons = []

            # Heuristic Rule 1: Forced Null Encryption
            if not tower.encrypted:
                suspicious = True
                reasons.append("ENCRYPTION_DISABLED_A50")

            # Heuristic Rule 2: Exceptionally Strong Signal with Abnormal LAC
            if tower.signal_power_dbm > -48.0 and tower.lac == 9999:
                suspicious = True
                reasons.append("HIGH_POWER_ROGUE_LAC")

            # Heuristic Rule 3: Zero TA anomaly forcing mobile station reconnect
            if tower.ta == 0 and tower.signal_power_dbm > -55.0:
                suspicious = True
                reasons.append("ZERO_TA_IMSI_CATCHER_PATTERN")

            tower.is_suspicious = suspicious
            tower.flag_reason = " | ".join(reasons) if reasons else "CLEAN"
            processed_towers.append(tower)

            if suspicious:
                self.log(f"ALERT: Rogue Base Station Detected! CID: {tower.cell_id} | Flags: {tower.flag_reason}", level="CRITICAL")
            else:
                self.log(f"Tower Verified: CID {tower.cell_id} (MCC: {tower.mcc}, MNC: {tower.mnc})", level="OK")

        return processed_towers


# ==============================================================================
# MAIN EXECUTION ROUTINE
# ==============================================================================

def main():
    print("""
    ┌────────────────────────────────────────────────────────┐
    │     SIGNAL-SCOPE & CELLULAR NETWORK ANALYSIS TOOL      │
    │            Wireless & Hardware Security                │
    │             Coded by Mr. Sabaz Ali Khan                │
    └────────────────────────────────────────────────────────┘
    """)

    engine = SignalScopeEngine(interface="sdr_hackrf_0")

    # Step 1: Perform Spectrum Sweep
    engine.log("Initializing Software Defined Radio (SDR) Hardware Interface...")
    time.sleep(0.5)
    engine.log("Executing RF Spectrum Sweep over GSM900 Band (930 MHz - 950 MHz)...")
    spectrum_data = engine.scan_rf_spectrum(start_freq_mhz=930.0, stop_freq_mhz=950.0, step_mhz=0.5)
    
    # Step 2: Render Spectrum Graph
    engine.render_ascii_spectrum(spectrum_data)

    # Step 3: Cellular Network Monitor & Rogue Base Station Detection
    engine.log("Capturing GSM/LTE Broadcast Control Channels (BCCH)...")
    
    sample_towers = [
        CellTower(cell_id=10421, mcc=410, mnc=1, lac=4301, frequency_mhz=935.2, signal_power_dbm=-78.5, ta=2, encrypted=True),
        CellTower(cell_id=10422, mcc=410, mnc=1, lac=4301, frequency_mhz=937.8, signal_power_dbm=-82.1, ta=3, encrypted=True),
        CellTower(cell_id=66666, mcc=410, mnc=1, lac=9999, frequency_mhz=948.6, signal_power_dbm=-42.0, ta=0, encrypted=False),
    ]

    analyzed_towers = engine.analyze_cellular_towers(sample_towers)

    # Step 4: Summary Table
    print("\n" + "=" * 78)
    print(f"{'Cell ID':<10} | {'Freq (MHz)':<10} | {'Power':<10} | {'Encrypted':<10} | {'Status':<12} | {'Notes'}")
    print("=" * 78)
    for tower in analyzed_towers:
        status = "CRITICAL" if tower.is_suspicious else "SECURE"
        enc_str = "YES (A5/3)" if tower.encrypted else "NO (A5/0)"
        print(f"{tower.cell_id:<10} | {tower.frequency_mhz:<10.1f} | {tower.signal_power_dbm:<10.1f} | {enc_str:<10} | {status:<12} | {tower.flag_reason}")
    print("=" * 78)
    print("\n[+] Scan complete. Developer Signature: Coded by Mr. Sabaz Ali Khan\n")


if __name__ == "__main__":
    main()