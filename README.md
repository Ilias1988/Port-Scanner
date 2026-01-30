# 🔍 Port Scanner POC

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Purpose-Educational-orange.svg" alt="Purpose">
</p>

A **Proof of Concept** multithreaded port scanner written in Python for cybersecurity education and authorized penetration testing.

```
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
```

---

## ⚠️ Disclaimer

**IMPORTANT: This tool is provided for educational and authorized security testing purposes ONLY.**

- ❌ **DO NOT** use this tool on systems you don't own or don't have explicit written permission to scan
- ❌ Unauthorized port scanning is **illegal** in many jurisdictions
- ❌ The author is **NOT responsible** for any misuse or damage caused by this tool
- ✅ Always obtain **proper authorization** before scanning any network or system
- ✅ Use this tool **responsibly** and **ethically**

By using this tool, you agree to use it only for legal and authorized purposes.

---

## ✨ Features

- 🚀 **Multithreaded scanning** - Fast parallel port scanning with configurable threads
- 🎯 **Multiple scan modes** - Common ports, port ranges, or full 65535 port scan
- 📡 **Banner grabbing** - Attempts to identify services by grabbing banners
- 🔍 **Service detection** - Identifies well-known services (HTTP, SSH, FTP, etc.)
- 📊 **Clean output** - Colored terminal output with summary table
- 💾 **Export results** - Save scan results to a file
- ⚡ **Configurable timeout** - Adjust connection timeout for different network conditions

---

## 📋 Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/Ilias1988/port-scanner-poc.git
cd port-scanner-poc
```

### (Optional) Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📖 Usage

### Basic Usage

```bash
python port_scanner.py -t <target> -p <ports>
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--target` | `-t` | Target IP address or hostname | Required |
| `--ports` | `-p` | Ports to scan | `common` |
| `--threads` | `-T` | Number of threads | `100` |
| `--timeout` | | Connection timeout (seconds) | `1.0` |
| `--output` | `-o` | Save results to file | None |

### Port Options

| Option | Description |
|--------|-------------|
| `common` | Well-known ports (21, 22, 23, 25, 53, 80, 110, 443, etc.) |
| `top100` | Ports 1-100 + well-known ports |
| `all` | All ports (1-65535) - ⚠️ Very slow! |
| `1-1000` | Port range (e.g., 1 to 1000) |
| `80,443,8080` | Specific ports (comma-separated) |

---

## 💡 Examples

### Scan common ports on a target

```bash
python port_scanner.py -t 192.168.1.1 -p common
```

### Scan a port range

```bash
python port_scanner.py -t 192.168.1.1 -p 1-1000
```

### Scan specific ports

```bash
python port_scanner.py -t 192.168.1.1 -p 80,443,8080,3306
```

### Scan with more threads and save results

```bash
python port_scanner.py -t 192.168.1.1 -p common -T 200 -o results.txt
```

### Scan localhost

```bash
python port_scanner.py -t localhost -p top100
```

### Scan with custom timeout

```bash
python port_scanner.py -t 10.0.0.1 -p common --timeout 2.0
```

---

## 📸 Sample Output

```
============================================================
  🔍 PORT SCANNER - Cybersecurity POC
============================================================

  Target: 192.168.1.1 (192.168.1.1)
  Ports: 25 ports to scan
  Threads: 100
  Timeout: 1.0s
  Start Time: 2024-01-15 22:30:45

────────────────────────────────────────────────────────────
  Scanning in progress...

  [+] Port    22 - OPEN - SSH
  [+] Port    80 - OPEN - HTTP
  [+] Port   443 - OPEN - HTTPS

────────────────────────────────────────────────────────────

  ✅ Scan Completed!
  End Time: 2024-01-15 22:30:47

  📊 Open Ports Summary:
  Found 3 open ports

  ──────────────────────────────────────────────────
  │ Port     │ Service         │ Status       │
  ──────────────────────────────────────────────────
  │ 22       │ SSH             │ OPEN         │
  │ 80       │ HTTP            │ OPEN         │
  │ 443      │ HTTPS           │ OPEN         │
  ──────────────────────────────────────────────────

============================================================
```

---

## 🔧 Well-Known Ports Included

| Port | Service | Port | Service |
|------|---------|------|---------|
| 21 | FTP | 445 | SMB |
| 22 | SSH | 993 | IMAPS |
| 23 | Telnet | 995 | POP3S |
| 25 | SMTP | 1433 | MSSQL |
| 53 | DNS | 1521 | Oracle |
| 80 | HTTP | 3306 | MySQL |
| 110 | POP3 | 3389 | RDP |
| 111 | RPC | 5432 | PostgreSQL |
| 135 | MSRPC | 5900 | VNC |
| 139 | NetBIOS | 6379 | Redis |
| 143 | IMAP | 8080 | HTTP-Proxy |
| 443 | HTTPS | 27017 | MongoDB |

---

## 🛡️ Security Best Practices

1. **Always get authorization** before scanning any network
2. **Document your testing** and keep records of permission
3. **Use responsibly** - don't scan networks you don't own
4. **Respect rate limits** - excessive scanning can disrupt services
5. **Report vulnerabilities** responsibly to system owners

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

<p align="center">
  <strong>⚠️ Remember: Always scan responsibly and legally! ⚠️</strong>
</p>
