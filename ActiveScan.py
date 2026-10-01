#!/usr/bin/env python3
# =====================================================
#          ActiveScan MultiRadar
#   Multi-Threaded Active Network Radar Scanner
#   =====================================================
#   Coded by: Mr. Sabaz Ali Khan
#   Purpose: Active host discovery + port scanning
#            using multiple "radars" (threads)
#            for fast network reconnaissance.
#   Features:
#     • Multi-threaded ICMP ping sweep (Radar Mode)
#     • Multi-threaded TCP SYN / Connect port scan
#     • Supports single IP, IP range, or CIDR subnet
#     • Cross-platform (Windows / Linux)
#     • Colorful output + live progress
#     • No external dependencies (pure Python + stdlib)
#   Usage: python3 ActiveScan_MultiRadar.py -t 192.168.1.0/24 -p 1-1000 -th 200
# =====================================================

import argparse
import socket
import subprocess
import threading
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from ipaddress import ip_network, ip_address
from datetime import datetime

# ====================== COLORS ======================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
{Colors.HEADER}╔══════════════════════════════════════════════════════════════╗
║                ActiveScan MultiRadar v1.0                    ║
║          Multi-Threaded Active Network Radar                 ║
║                Coded by Mr. Sabaz Ali Khan                   ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
    """
    print(banner)
    print(f"{Colors.CYAN}[*] Starting ActiveScan MultiRadar at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")

# ====================== PING (Radar) ======================
def is_host_live(ip):
    """Active ICMP ping - works on both Windows and Linux"""
    param = '-n' if os.name == 'nt' else '-c'
    timeout = '-w' if os.name == 'nt' else '-W'
    timeout_val = '1' if os.name == 'nt' else '1'
    
    command = ['ping', param, '1', timeout, timeout_val, str(ip)]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=2)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

# ====================== PORT SCAN ======================
def scan_port(ip, port):
    """Active TCP Connect scan (most reliable cross-platform)"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((str(ip), port))
            if result == 0:
                try:
                    service = socket.getservbyport(port, 'tcp')
                except:
                    service = "unknown"
                return port, service
            return None
    except:
        return None

# ====================== MAIN SCANNER ======================
def active_scan(target, ports_range=(1, 1000), threads=100, radar_only=False):
    print(f"{Colors.YELLOW}[*] Target: {target}{Colors.ENDC}")
    print(f"{Colors.YELLOW}[*] Threads: {threads} | Port range: {ports_range[0]}-{ports_range[1]}{Colors.ENDC}\n")
    
    # Parse target (single IP, range or CIDR)
    try:
        network = ip_network(target, strict=False)
        hosts = list(network.hosts())
    except ValueError:
        # Single IP
        hosts = [ip_address(target)]
    
    print(f"{Colors.BLUE}[+] Scanning {len(hosts)} host(s) with {threads} radar threads...{Colors.ENDC}")
    
    live_hosts = []
    start_time = time.time()
    
    # Phase 1: Multi-Threaded Radar (Host Discovery)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_ip = {executor.submit(is_host_live, ip): ip for ip in hosts}
        completed = 0
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            completed += 1
            if completed % max(1, len(hosts)//10) == 0:  # Progress update
                progress = int((completed / len(hosts)) * 100)
                print(f"{Colors.CYAN}[RADAR] Progress: {progress}%{Colors.ENDC}", end="\r")
            
            try:
                if future.result():
                    live_hosts.append(ip)
                    print(f"{Colors.GREEN}[+] LIVE: {ip}{Colors.ENDC}")
            except:
                pass
    
    radar_time = time.time() - start_time
    print(f"\n{Colors.GREEN}[✓] Radar phase completed in {radar_time:.2f}s | Found {len(live_hosts)} live host(s){Colors.ENDC}\n")
    
    if radar_only or not live_hosts:
        return
    
    # Phase 2: Multi-Threaded Port Scanning on live hosts
    print(f"{Colors.BLUE}[+] Starting Active Port Scan on {len(live_hosts)} live host(s)...{Colors.ENDC}")
    
    open_ports = {}
    port_start, port_end = ports_range
    total_ports = port_end - port_start + 1
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for ip in live_hosts:
            print(f"{Colors.YELLOW}[*] Scanning ports on {ip}...{Colors.ENDC}")
            open_ports[ip] = []
            futures = {executor.submit(scan_port, ip, port): port for port in range(port_start, port_end + 1)}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    port, service = result
                    open_ports[ip].append((port, service))
                    print(f"{Colors.GREEN}    └── OPEN: {port:5} → {service}{Colors.ENDC}")
    
    # Final Report
    total_time = time.time() - start_time
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}                  ActiveScan MultiRadar REPORT{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time taken : {total_time:.2f} seconds")
    print(f"Live hosts       : {len(live_hosts)}")
    print(f"Threads used     : {threads}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    
    if open_ports:
        for ip, ports in open_ports.items():
            if ports:
                print(f"\n{Colors.GREEN}[+] Results for {ip}{Colors.ENDC}")
                for port, service in sorted(ports):
                    print(f"    {Colors.GREEN}PORT {port:5} OPEN → {service}{Colors.ENDC}")
    else:
        print(f"\n{Colors.YELLOW}[!] No open ports found in the scanned range.{Colors.ENDC}")

# ====================== CLI ======================
def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="ActiveScan MultiRadar - Coded by Mr. Sabaz Ali Khan")
    parser.add_argument("-t", "--target", required=True, help="Target IP, range (192.168.1.1-254) or CIDR (192.168.1.0/24)")
    parser.add_argument("-p", "--ports", type=str, default="1-1000", help="Port range (default: 1-1000)")
    parser.add_argument("-th", "--threads", type=int, default=150, help="Number of threads (default: 150)")
    parser.add_argument("-r", "--radar-only", action="store_true", help="Only run radar (host discovery), skip port scan")
    
    args = parser.parse_args()
    
    # Parse port range
    try:
        if '-' in args.ports:
            p_start, p_end = map(int, args.ports.split('-'))
        else:
            p_start = p_end = int(args.ports)
    except:
        p_start, p_end = 1, 1000
    
    active_scan(args.target, (p_start, p_end), args.threads, args.radar_only)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Scan interrupted by user. Exiting...{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {e}{Colors.ENDC}")