#!/usr/bin/env python3
"""
CamAudit X – Advanced CCTV Security Auditor
Coded by Cyber Security Engineer Mr Sabaz Ali Khan
"""

import sys
import socket
import threading
import base64
import argparse
import time
import random
import os
from datetime import datetime

try:
    import requests
    from requests.auth import HTTPDigestAuth
except ImportError:
    print("[!] Install dependencies: pip install requests")
    sys.exit(1)

# ============ CONFIG ============
VERSION = "1.0"
AUTHOR = "Mr Sabaz Ali Khan"
TOOL = "CamAudit X"

RTSP_PORTS = [554, 8554, 8001, 8080, 10554]
HTTP_PORTS = [80, 8080, 8000, 81, 88, 443, 7550]

DEFAULT_CREDS = [
    ("admin", "admin"), ("admin", "12345"), ("admin", "123456"),
    ("admin", "password"), ("admin", ""), ("admin", "admin123"),
    ("root", "root"), ("root", "pass"), ("admin", "9999"),
    ("admin", "1234"), ("administrator", "admin"), ("admin", "4321"),
    ("666666", "666666"), ("888888", "888888"), ("admin", "meinsm"),
    ("service", "service"), ("supervisor", "supervisor"),
]

RTSP_PATHS = ["/", "/live", "/h264", "/stream1", "/cam/realmonitor?channel=1&subtype=0",
              "/LiveChannels/1/live", "/live1.264", "/ch01/0", "/video1",
              "/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "CamAuditX/1.0 (Security Auditor)",
    "Lavf/58.29.100",
]

lock = threading.Lock()
results = []

# ============ MATRIX BANNER ============
GREEN = "\033[1;32m"
RED = "\033[1;31m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"
DIM = "\033[2m"

BANNER = f"""{GREEN}
  ██████╗ █████╗ ███╗   ██╗ █████╗ ██╗   ██╗██╗████████╗   ██╗  ██╗
 ██╔════╝██╔══██╗████╗  ██║██╔══██╗╚██╗ ██╔╝██║╚══██╔══╝   ╚██╗██╔╝
 ██║     ███████║██╔██╗ ██║███████║ ╚████╔╝ ██║   ██║       ╚███╔╝ 
 ██║     ██╔══██║██║╚██╗██║██╔══██║  ╚██╔╝  ██║   ██║       ██╔██╗ 
 ╚██████╗██║  ██║██║ ╚████║██║  ██║   ██║   ██║   ██║       ██╔╝██╗
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝   ╚═╝       ╚═╝ ╚═╝
{CYAN}          [+] Advanced CCTV Security Auditor v{VERSION} [+]
       ╔═══════════════════════════════════════════════════╗
       ║  Coded by Cyber Security Engineer Mr Sabaz Ali Khan ║
       ╚═══════════════════════════════════════════════════╝{RESET}
{DIM}       >>> Anonymous Mode Activated | Stay In Shadows <<<{RESET}
"""

def matrix_rain(duration=2):
    """Short matrix effect before scan"""
    cols = os.get_terminal_size().columns
    chars = "01アカサタナハマヤラ01ABCD#@$%&"
    end = time.time() + duration
    print(DIM)
    while time.time() < end:
        line = "".join(random.choice(chars) if random.random() > 0.9 else " " for _ in range(cols))
        print(line)
        time.sleep(0.04)
    print(RESET)

# ============ SCANNING ============
def tcp_open(ip, port, timeout=2):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        if s.connect_ex((ip, port)) == 0:
            s.close()
            return True
        s.close()
    except Exception:
        pass
    return False

def get_rtsp_options(ip, port, path, auth=None, timeout=3):
    """Send RTSP OPTIONS/DESCRIBE request, return response"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        cseq = random.randint(1, 99)
        req = f"OPTIONS rtsp://{ip}:{port}{path} RTSP/1.0\r\nCSeq: {cseq}\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\n\r\n"
        s.send(req.encode())
        resp = s.recv(2048).decode(errors="ignore")
        s.close()
        return resp
    except Exception:
        return None

def rtsp_unauth_check(ip, port):
    """Check for unauthenticated RTSP stream access"""
    for path in RTSP_PATHS:
        req = f"DESCRIBE rtsp://{ip}:{port}{path} RTSP/1.0\r\nCSeq: 2\r\nAccept: application/sdp\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\n\r\n"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            s.send(req.encode())
            resp = s.recv(4096).decode(errors="ignore")
            s.close()
            if "200 OK" in resp:
                return (path, "UNAUTHENTICATED", resp)
            elif "401" in resp:
                return (path, "AUTH_REQUIRED", resp)
        except Exception:
            continue
    return None

def rtsp_bruteforce(ip, port, path):
    """Try default credentials against RTSP DESCRIBE"""
    for user, pwd in DEFAULT_CREDS:
        token = base64.b64encode(f"{user}:{pwd}".encode()).decode()
        req = (f"DESCRIBE rtsp://{ip}:{port}{path} RTSP/1.0\r\n"
               f"CSeq: 3\r\nAuthorization: Basic {token}\r\n"
               f"Accept: application/sdp\r\n\r\n")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            s.send(req.encode())
            resp = s.recv(4096).decode(errors="ignore")
            s.close()
            if "200 OK" in resp:
                return (user, pwd)
        except Exception:
            continue
    return None

def http_audit(ip, port, timeout=3):
    """Check HTTP camera interface: default creds + info leak"""
    found = []
    scheme = "https" if port == 443 else "http"
    base = f"{scheme}://{ip}:{port}"
    try:
        r = requests.get(base, timeout=timeout, verify=False)
        server = r.headers.get("Server", "Unknown")
        with lock:
            print(f"  {YELLOW}[HTTP]{RESET} {base} | Server: {CYAN}{server}{RESET} | Title check...")
        # look for camera vendor fingerprint
        for vendor in ["Hikvision", "Dahua", "Axis", "Foscam", "TP-Link", "Vivotek", "CP Plus"]:
            if vendor.lower() in r.text.lower():
                with lock:
                    print(f"  {GREEN}[FINGERPRINT]{RESET} Vendor detected: {CYAN}{vendor}{RESET} at {base}")
                break
        # try default creds on common login endpoints
        for ep in ["/api/login", "/login", "/api/user/login", "/cgi-bin/gw.cgi"]:
            for user, pwd in DEFAULT_CREDS[:6]:
                try:
                    rr = requests.post(f"{base}{ep}", data={"username": user, "password": pwd},
                                       timeout=2, verify=False)
                    if rr.status_code in (200, 302) and "fail" not in rr.text.lower():
                        found.append((user, pwd, ep))
                        break
                except Exception:
                    continue
    except Exception:
        pass
    return found

def audit_camera(ip):
    """Full audit pipeline for one camera host"""
    with lock:
        print(f"\n{CYAN}[*] Auditing:{RESET} {ip}")
    open_ports = []
    for p in RTSP_PORTS + HTTP_PORTS:
        if tcp_open(ip, p):
            open_ports.append(p)
            with lock:
                print(f"  {GREEN}[OPEN]{RESET} Port {p}")

    for port in [p for p in open_ports if p in RTSP_PORTS]:
        check = rtsp_unauth_check(ip, port)
        if check:
            path, status, resp = check
            if status == "UNAUTHENTICATED":
                with lock:
                    print(f"  {RED}[CRITICAL]{RESET} Open RTSP stream WITHOUT auth: rtsp://{ip}:{port}{path}")
                    results.append((ip, port, "RTSP-NO-AUTH", path))
            else:
                with lock:
                    print(f"  {YELLOW}[INFO]{RESET} RTSP requires auth, trying defaults...")
                creds = rtsp_bruteforce(ip, port, path)
                if creds:
                    with lock:
                        print(f"  {RED}[CRITICAL]{RESET} Default creds work: {creds[0]}:{creds[1]} @ rtsp://{ip}:{port}{path}")
                        results.append((ip, port, "RTSP-DEFAULT-CREDS", f"{creds[0]}:{creds[1]}"))
                else:
                    with lock:
                        print(f"  {GREEN}[OK]{RESET} RTSP creds not bypassed with defaults")

    for port in [p for p in open_ports if p in HTTP_PORTS]:
        findings = http_audit(ip, port)
        for user, pwd, ep in findings:
            with lock:
                print(f"  {RED}[CRITICAL]{RESET} HTTP default creds: {user}:{pwd} via {ep}")
                results.append((ip, port, "HTTP-DEFAULT-CREDS", f"{user}:{pwd}"))

# ============ REPORT ============
def save_report(output_file):
    if not results:
        print(f"\n{YELLOW}[!]{RESET} No findings to report.")
        return
    with open(output_file, "w") as f:
        f.write(f"CamAudit X Report - {datetime.now()}\n")
        f.write(f"Coded by Mr Sabaz Ali Khan\n{'='*60}\n")
        for ip, port, issue, detail in results:
            f.write(f"[{issue}] {ip}:{port} -> {detail}\n")
    print(f"\n{GREEN}[+]{RESET} Report saved: {output_file}")

# ============ MAIN ============
def main():
    parser = argparse.ArgumentParser(
        prog="CamAudit X",
        description="Advanced CCTV Security Auditor - by Mr Sabaz Ali Khan",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-t", "--target", help="Single IP or CIDR range (e.g. 192.168.1.0/24)")
    parser.add_argument("-f", "--file", help="File with target IPs (one per line)")
    parser.add_argument("-o", "--output", default="camaudit_report.txt", help="Output report file")
    parser.add_argument("--no-matrix", action="store_true", help="Skip matrix intro")
    args = parser.parse_args()

    print(BANNER)
    if not args.no_matrix:
        matrix_rain(2)

    targets = []
    if args.target:
        if "/" in args.target:  # CIDR
            import ipaddress
            targets = [str(h) for h in ipaddress.ip_network(args.target, strict=False).hosts()]
        else:
            targets = [args.target]
    elif args.file:
        with open(args.file) as f:
            targets = [l.strip() for l in f if l.strip()]
    else:
        parser.print_help()
        sys.exit(1)

    print(f"{GREEN}[+]{RESET} Loaded {len(targets)} target(s). Scanning...")
    threads = []
    for ip in targets[:50]:  # safety cap
        t = threading.Thread(target=audit_camera, args=(ip,))
        t.start()
        threads.append(t)
        time.sleep(0.1)

    for t in threads:
        t.join()

    print(f"\n{'='*60}")
    print(f"{GREEN}[*] Scan complete.{RESET} Findings: {len(results)}")
    save_report(args.output)
    print(f"{DIM}\n  -- CamAudit X | Coded by Mr Sabaz Ali Khan --{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!]{RESET} Aborted by user. Exiting...")
        sys.exit(0)
