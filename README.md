<div align="center">

<img src="docs/banner.svg" alt="Maelstrom" width="800">

# Maelstrom

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2196F3.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-249%20passing-brightgreen.svg)](tests/)

Maelstrom is a NetExec wrapper that combines 35+ enumeration modules across SMB, LDAP, MSSQL, RDP, FTP, and NFS into a single command — with colored output, intelligent credential handling, multi-target scanning, and actionable next-step recommendations. Think of it as enum4linux-ng on steroids, powered by NetExec.

</div>

---

## Table of Contents

- [Highlights](#highlights)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Modules](#modules)
- [Security](#security)
- [Configuration](#configuration)
- [Example Output](#example-output)
- [Testing](#testing)
- [Contributing](#contributing)

---

## Highlights

<table>
<tr>
<td width="50%">

### 35+ Modules

Users, groups, shares, LAPS, Kerberoastable, delegation, ADCS, gMSA, GPP, PSO, SCCM, and more. Run all at once or pick specific modules with flags.

</td>
<td width="50%">

### Multi-Protocol

SMB, LDAP, MSSQL, RDP, FTP, NFS, and VNC enumeration in a single scan. Port availability is auto-detected before each module runs.

</td>
</tr>
<tr>
<td width="50%">

### Multi-Target Scanning

CIDR ranges, IP ranges, and target files. Parallel host discovery scans /24 networks in seconds. Per-target results with aggregate summary.

</td>
<td width="50%">

### Multi-Credential Mode

Test multiple credentials with `-C creds.txt`. Visual share access matrix, admin detection, and access comparison across users.

</td>
</tr>
<tr>
<td width="50%">

### Actionable Next Steps

Findings generate ready-to-run commands with your credentials auto-filled. Priority-ranked with auto-exploit warnings for dangerous modules.

</td>
<td width="50%">

### Copy-Paste Output

Clean line-by-line lists of usernames, SPNs, shares, computers, and more. Pipe directly to other tools or save to files.

</td>
</tr>
<tr>
<td width="50%">

### Zero Dependencies

Only requires Python 3.10+ and NetExec on your PATH. No pip packages, no virtual environments, no build steps.

</td>
<td width="50%">

### Proxy Mode

Full proxychains/SOCKS support. Auto-reduces concurrency, increases timeouts, and skips incompatible modules. Auto-detected via `LD_PRELOAD`.

</td>
</tr>
</table>

---

## Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | >= 3.10 |
| NetExec | Latest (in PATH) |
| Platform | Linux, macOS, Windows |

### Install

```bash
# pipx (recommended — isolated environment)
pipx install git+https://github.com/Real-Fruit-Snacks/maelstrom.git

# pip
pip install git+https://github.com/Real-Fruit-Snacks/maelstrom.git

# Development
git clone https://github.com/Real-Fruit-Snacks/maelstrom.git
cd maelstrom
pip install -e .
```

```bash
# Anonymous — auto-probes null/guest sessions
maelstrom 10.0.0.1

# Single credential — full enumeration
maelstrom 10.0.0.1 -u admin -p 'Password123' -d CORP

# Pass-the-hash
maelstrom 10.0.0.1 -u admin -H aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0

# Multi-credential — compare access levels
maelstrom 10.0.0.1 -C creds.txt -d CORP

# Multi-target — CIDR, range, or file
maelstrom 10.0.0.0/24 -u admin -p 'Password123'
maelstrom targets.txt -u admin -p 'Password123'

# Discover live SMB hosts only (no creds required)
maelstrom 10.0.0.0/24 --discover-only

# Specific modules only
maelstrom 10.0.0.1 -u admin -p pass --shares --users --laps --mssql
```

### Development

```bash
pytest tests/ -v              # All 249 tests
pytest tests/ --cov=maelstrom # With coverage
black maelstrom/ tests/       # Format code
flake8 maelstrom/ tests/ --max-line-length=100
```

---

## Architecture

Maelstrom is a pure Python CLI tool with zero external dependencies. It shells out to NetExec (`nxc`) for all network operations and parses the output.

```
maelstrom/
├── maelstrom/
│   ├── __init__.py           # Version, package init
│   ├── __main__.py           # python -m maelstrom entry
│   ├── cli/
│   │   ├── args.py           # Argument parsing (70+ flags)
│   │   └── main.py           # Orchestration, module dispatch
│   ├── core/
│   │   ├── colors.py         # Catppuccin Mocha terminal colors
│   │   ├── constants.py      # Regex patterns, thread pool sizes
│   │   ├── output.py         # Buffered output system
│   │   ├── parallel.py       # ThreadPoolExecutor module runner
│   │   └── runner.py         # NetExec subprocess execution
│   ├── enums/                # 35+ enumeration modules
│   ├── models/               # EnumCache, Credential, results
│   ├── parsing/              # NXC output parsers
│   ├── reporting/            # Summary, next steps, share matrix
│   └── validation/           # Credential & anonymous validation
└── tests/                    # 249 tests
```

### Execution Flow

| Phase | Description |
|-------|-------------|
| 1. Pre-scan | Port 445 scan, SMB validation (for multi-target) |
| 2. Pre-flight | SMB reachability, hostname resolution check |
| 3. Auth probe | Anonymous session (null/guest/LDAP) or credential validation |
| 4. Cache prime | 7 parallel queries: SMB, RID brute, LDAP, pass policy, etc. |
| 5. Sequential | Domain intel, SMB info, users, groups |
| 6. Parallel | 36 independent modules via ThreadPoolExecutor (15 workers) |
| 7. Reports | Executive summary, next steps, share matrix, copy-paste |

### Threading Model

| Level | Workers | Purpose |
|-------|---------|---------|
| Module-level | 15 | Independent enum modules in parallel |
| Target-level | 5 | Multiple targets scanned concurrently |
| Port prescan | 100 | Fast TCP port 445 filtering |
| Proxy mode | 2 | Reduced for SOCKS/proxychains compatibility |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.10+ (zero external deps) |
| **Engine** | NetExec (nxc) via subprocess |
| **Parallelism** | ThreadPoolExecutor (stdlib) |
| **Colors** | Catppuccin Mocha (24-bit true color) |
| **Output** | enum4linux-ng style indicators |
| **Testing** | pytest, unittest |
| **Formatting** | Black, isort, flake8 |

---

## Modules

| Module | Description |
|--------|-------------|
| Users | Domain users via RPC with built-in/service/domain categorization |
| Groups | Domain groups with high-value highlighting and members |
| Local Groups | Local groups and Administrators members |
| Computers | Domain computers with OS info and outdated detection |
| Shares | SMB share permissions (matrix in multi-cred mode) |
| Spider | Recursive file listing on shares (metadata or download) |
| Policies | Password and lockout policies |
| Sessions | Active Windows sessions `[admin]` |
| Logged On | Currently logged on users `[admin]` |
| Printers | Print spooler status with PrintNightmare warning |
| AV/EDR | Installed security products `[admin]` |
| LAPS | LAPS deployment and password read permissions |
| LDAP Signing | Signing and channel binding requirements |
| Pre-2K Computers | Computers with weak default passwords |
| BitLocker | Drive encryption status `[admin]` |
| Kerberoastable | Accounts with SPNs via LDAP query |
| AS-REP Roastable | Accounts without pre-authentication |
| Delegation | Unconstrained/constrained/RBCD delegation |
| ADCS | Certificate templates and certificate authorities |
| DC List | Domain controllers and trust relationships |
| AdminCount | Accounts with adminCount=1 |
| PASSWD_NOTREQD | Accounts without password requirement |
| gMSA | Group Managed Service Account enumeration |
| GPP Password | Group Policy Preferences cpassword extraction (MS14-025) |
| PSO | Fine-Grained Password Policies (Password Settings Objects) |
| SCCM | SCCM/MECM infrastructure discovery |
| MAQ | Machine Account Quota check |
| WebDAV | WebClient service status check |
| DNS | DNS enumeration recommendations (passive) |
| Descriptions | User description fields (password hunting) |
| SMB Signing | SMB signing requirements |
| Subnets | AD sites and network topology |
| Network Interfaces | Multi-homed host detection via SMB IOCTL |
| Disks | Disk drive enumeration via RPC `[admin]` |
| MSSQL | Service detection, auth test, query recommendations |
| RDP | RDP status and NLA requirements |
| FTP | Anonymous access and credential testing |
| NFS | NFS exports and permissions |
| VNC | VNC service detection (ports 5900-5903, 5800-5801) |
| iOXID | Multi-homed host discovery via DCOM (port 135) |

---

## Security

| Principle | Implementation |
|-----------|----------------|
| **Read-only** | LDAP queries, SMB enumeration, RPC calls — never executes commands on targets |
| **No exploitation** | Kerberoasting finds SPNs via LDAP only — doesn't request TGS tickets |
| **Credential safety** | Output files created with 0o600 permissions, warns on permissive cred files |
| **Recommendations only** | MSSQL tests auth only, shows SQL queries for manual execution |
| **Auto-exploit warnings** | Next steps flag commands that automatically exploit (secretsdump, ntlmrelayx) |

---

## Configuration

| Category | Key Flags | Description |
|----------|-----------|-------------|
| Target | `TARGET` | IP, hostname, CIDR, range, or target file (auto-detected) |
| Auth | `-u -p -H -d` | Username, password, NTLM hash, domain |
| Kerberos | `-k --use-kcache --aesKey` | Kerberos auth, ccache, AES keys |
| Certs | `--pfx-cert --pem-cert` | Certificate-based PKINIT auth |
| Multi-cred | `-C -U -P` | Credential files with spray controls |
| Modules | `-A --shares --users --laps` | Select specific or all modules |
| Security | `--delegation --adcs --kerberoast` | Security-focused checks |
| Protocols | `--mssql --rdp --ftp --nfs` | Additional protocol enumeration |
| Output | `-o -j --copy-paste` | File output, JSON, copy-paste lists |
| Behavior | `--proxy-mode --debug --timeout` | Runtime behavior controls |

---

## Example Output

### Security Findings

```
LDAP SECURITY CONFIGURATION
--------------------------------------------------
  [!] LDAP Signing: NOT REQUIRED
      Vulnerable to LDAP relay attacks

  [!] Channel Binding: NOT ENFORCED
      May be vulnerable to certain relay attacks

LAPS DEPLOYMENT CHECK
--------------------------------------------------
[+] Found 15 computer(s) with LAPS configured
[!] Current user CAN read LAPS passwords!
    This indicates high privileges (Domain Admin, LAPS readers, etc.)
```

### Share Access Matrix (Multi-Credential)

```
Share         faraday     admin       svc_backup
------------- ----------  ----------  ----------
ADMIN$        -           READ,WRITE  -
C$            -           READ,WRITE  -
IPC$          READ        READ        READ
NETLOGON      READ        READ        READ
SYSVOL        READ        READ        READ
Backups$      READ        READ,WRITE  READ,WRITE

Legend: WRITE (green) | READ (yellow) | - = No Access

[!] Non-default share 'Backups$' accessible by: admin (RW), svc_backup (RW), faraday (R)
```

---

## Testing

```bash
pytest tests/ -v                        # All 249 tests
pytest tests/test_parsing.py -v         # Single file
pytest tests/ --cov=maelstrom           # With coverage
pytest tests/ -m "not slow"             # Skip slow tests
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run `black maelstrom/ tests/ && pytest tests/ -v` — both must pass
5. Commit with descriptive message
6. Open a Pull Request

- Python 3.10+ with Black formatting (100 char lines)
- Catppuccin Mocha color palette for all terminal output
- enum4linux-ng style indicators: `[*]` info, `[+]` success, `[-]` error, `[!]` warning
- Pure reconnaissance only — never execute commands on targets

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

<div align="center">

**Built for reconnaissance. Powered by NetExec.**

[GitHub](https://github.com/Real-Fruit-Snacks/maelstrom) | [License (MIT)](LICENSE) | [Report Issue](https://github.com/Real-Fruit-Snacks/maelstrom/issues)

*Maelstrom — comprehensive AD enumeration in a single command*

</div>
