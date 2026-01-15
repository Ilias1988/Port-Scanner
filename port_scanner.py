#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║                    🔍 PORT SCANNER POC                        ║
║                  Cybersecurity Tool - Python                  ║
╚═══════════════════════════════════════════════════════════════╝

Description: Proof of Concept Port Scanner for network port scanning
Author: Cybersecurity POC
Language: Python 3

⚠️  WARNING: Use this tool ONLY on systems you have authorization 
    to scan. Unauthorized scanning is illegal!
"""

import socket
import threading
import argparse
import sys
from datetime import datetime
from queue import Queue
from typing import List, Tuple

# Terminal colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Well-known ports and their services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    111: "RPC",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
    27017: "MongoDB"
}

class PortScanner:
    """
    Port scanning class with multithreading support
    """
    
    def __init__(self, target: str, ports: List[int], threads: int = 100, timeout: float = 1.0):
        """
        Initialize the scanner
        
        Args:
            target: Target IP address or hostname
            ports: List of ports to scan
            threads: Number of threads (default: 100)
            timeout: Connection timeout in seconds (default: 1.0)
        """
        self.target = target
        self.ports = ports
        self.threads = threads
        self.timeout = timeout
        self.open_ports: List[Tuple[int, str]] = []
        self.port_queue = Queue()
        self.lock = threading.Lock()
        
    def resolve_target(self) -> str:
        """Resolve hostname to IP address"""
        try:
            ip = socket.gethostbyname(self.target)
            return ip
        except socket.gaierror:
            return None
            
    def get_service_name(self, port: int) -> str:
        """Returns the service name for a port"""
        if port in COMMON_PORTS:
            return COMMON_PORTS[port]
        try:
            return socket.getservbyport(port)
        except:
            return "Unknown"
    
    def grab_banner(self, sock: socket.socket, port: int) -> str:
        """
        Attempt to grab banner from the service
        """
        try:
            # Send a simple request for HTTP
            if port in [80, 8080, 8443, 443]:
                sock.send(b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n")
            else:
                sock.send(b"\r\n")
            
            sock.settimeout(2)
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner[:100] if banner else ""  # Limit size
        except:
            return ""
    
    def scan_port(self, port: int) -> bool:
        """
        Scan a specific port
        
        Args:
            port: Port number
            
        Returns:
            True if port is open, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                service = self.get_service_name(port)
                banner = self.grab_banner(sock, port)
                
                with self.lock:
                    self.open_ports.append((port, service, banner))
                    print(f"  {Colors.GREEN}[+] Port {port:5d} - OPEN - {service}{Colors.RESET}")
                    if banner:
                        print(f"      {Colors.CYAN}Banner: {banner[:60]}...{Colors.RESET}")
                
                sock.close()
                return True
            
            sock.close()
            return False
            
        except socket.timeout:
            return False
        except Exception as e:
            return False
    
    def worker(self):
        """Worker thread for scanning ports from queue"""
        while True:
            port = self.port_queue.get()
            if port is None:
                break
            self.scan_port(port)
            self.port_queue.task_done()
    
    def run(self) -> List[Tuple[int, str]]:
        """
        Execute the scan
        
        Returns:
            List of open ports and their services
        """
        # Resolve IP
        ip = self.resolve_target()
        if not ip:
            print(f"{Colors.RED}[!] Unable to resolve hostname: {self.target}{Colors.RESET}")
            return []
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}  🔍 PORT SCANNER - Cybersecurity POC{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"\n  {Colors.YELLOW}Target:{Colors.RESET} {self.target} ({ip})")
        print(f"  {Colors.YELLOW}Ports:{Colors.RESET} {len(self.ports)} ports to scan")
        print(f"  {Colors.YELLOW}Threads:{Colors.RESET} {self.threads}")
        print(f"  {Colors.YELLOW}Timeout:{Colors.RESET} {self.timeout}s")
        print(f"  {Colors.YELLOW}Start Time:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n{Colors.CYAN}{'─'*60}{Colors.RESET}")
        print(f"  {Colors.BOLD}Scanning in progress...{Colors.RESET}\n")
        
        # Add ports to queue
        for port in self.ports:
            self.port_queue.put(port)
        
        # Create and start threads
        threads = []
        for _ in range(min(self.threads, len(self.ports))):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Wait for completion
        self.port_queue.join()
        
        # Terminate threads
        for _ in threads:
            self.port_queue.put(None)
        for t in threads:
            t.join()
        
        # Results
        print(f"\n{Colors.CYAN}{'─'*60}{Colors.RESET}")
        print(f"\n  {Colors.BOLD}{Colors.GREEN}✅ Scan Completed!{Colors.RESET}")
        print(f"  {Colors.YELLOW}End Time:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.open_ports:
            print(f"\n  {Colors.BOLD}📊 Open Ports Summary:{Colors.RESET}")
            print(f"  {Colors.GREEN}Found {len(self.open_ports)} open ports{Colors.RESET}\n")
            
            # Sort by port number
            self.open_ports.sort(key=lambda x: x[0])
            
            print(f"  {'─'*50}")
            print(f"  │ {'Port':<8} │ {'Service':<15} │ {'Status':<12} │")
            print(f"  {'─'*50}")
            for port, service, _ in self.open_ports:
                print(f"  │ {port:<8} │ {service:<15} │ {Colors.GREEN}OPEN{Colors.RESET}         │")
            print(f"  {'─'*50}")
        else:
            print(f"\n  {Colors.YELLOW}⚠️  No open ports found in the scanned range{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}\n")
        
        return self.open_ports


def parse_ports(port_arg: str) -> List[int]:
    """
    Parse port argument
    Supports: 80, 80-100, 80,443,8080, common
    """
    ports = []
    
    if port_arg.lower() == 'common':
        return list(COMMON_PORTS.keys())
    
    if port_arg.lower() == 'all':
        return list(range(1, 65536))
    
    if port_arg.lower() == 'top100':
        return list(range(1, 101)) + list(COMMON_PORTS.keys())
    
    for part in port_arg.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    
    return sorted(list(set(ports)))


def main():
    """Main function"""
    
    banner = f"""
{Colors.CYAN}
    ╔════════════════════════════════════════════════════════════════════╗
    ║  ██████╗  ██████╗ ██████╗ ████████╗                                ║
    ║  ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝                                ║
    ║  ██████╔╝██║   ██║██████╔╝   ██║                                   ║
    ║  ██╔═══╝ ██║   ██║██╔══██╗   ██║                                   ║
    ║  ██║     ╚██████╔╝██║  ██║   ██║                                   ║
    ║  ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝                                   ║
    ║                                                                    ║
    ║  ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗       ║
    ║  ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗      ║
    ║  ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝      ║
    ║  ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗      ║
    ║  ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║      ║
    ║  ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝      ║
    ╚════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
    {Colors.YELLOW}🔒 Cybersecurity POC - Port Scanner Tool{Colors.RESET}
    {Colors.RED}⚠️  Use ONLY with authorization!{Colors.RESET}
    """
    
    print(banner)
    
    parser = argparse.ArgumentParser(
        description='🔍 Port Scanner POC - Network Port Scanning Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.YELLOW}Usage Examples:{Colors.RESET}
  python port_scanner.py -t 192.168.1.1 -p 80,443,8080
  python port_scanner.py -t example.com -p 1-1000
  python port_scanner.py -t 10.0.0.1 -p common
  python port_scanner.py -t localhost -p top100 -T 200

{Colors.CYAN}Port Options:{Colors.RESET}
  common  : Well-known ports (21,22,23,25,53,80,110,443,...)
  top100  : Ports 1-100 + well-known ports
  all     : All ports (1-65535) - ⚠️ SLOW!
  1-100   : Port range
  80,443  : Specific ports
        """
    )
    
    parser.add_argument('-t', '--target', required=True, 
                        help='Target IP address or hostname')
    parser.add_argument('-p', '--ports', default='common',
                        help='Ports to scan (default: common)')
    parser.add_argument('-T', '--threads', type=int, default=100,
                        help='Number of threads (default: 100)')
    parser.add_argument('--timeout', type=float, default=1.0,
                        help='Connection timeout in seconds (default: 1.0)')
    parser.add_argument('-o', '--output', 
                        help='Save results to file')
    
    args = parser.parse_args()
    
    # Parse ports
    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print(f"{Colors.RED}[!] Error parsing ports: {e}{Colors.RESET}")
        sys.exit(1)
    
    # Create and run scanner
    scanner = PortScanner(
        target=args.target,
        ports=ports,
        threads=args.threads,
        timeout=args.timeout
    )
    
    try:
        open_ports = scanner.run()
        
        # Save to file if requested
        if args.output and open_ports:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"Port Scanner Results - {args.target}\n")
                f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                for port, service, banner in open_ports:
                    f.write(f"Port {port}: {service} - OPEN\n")
                    if banner:
                        f.write(f"  Banner: {banner}\n")
            print(f"{Colors.GREEN}[+] Results saved to: {args.output}{Colors.RESET}")
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Scan interrupted by user{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
