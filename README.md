<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-light.svg">
  <img alt="Maelstrom" src="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-dark.svg" width="520">
</picture>

![Python](https://img.shields.io/badge/language-Python-3776AB.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**NetExec wrapper combining 35+ AD enumeration modules into a single command**

Shells out to NetExec for SMB, LDAP, MSSQL, RDP, FTP, NFS, and VNC enumeration with colored Catppuccin Mocha output, intelligent credential handling, multi-target scanning across CIDR ranges, and actionable next-step recommendations with auto-filled credentials.

> **Authorization Required**: This tool is designed for authorized security testing with explicit written permission. Unauthorized network enumeration is illegal and may result in criminal prosecution.

[Quick Start](#quick-start) • [Modules](#modules) • [Architecture](#architecture) • [Configuration](#configuration) • [Security](#security)

</div>

---

## Highlights

<table>
<tr>
<td width="50%">

**35+ Enumeration Modules**
Users, groups, shares, LAPS, Kerberoastable, delegation, ADCS, gMSA, GPP, PSO, SCCM, and more. Run all at once with `-A` or pick specific modules with individual flags.

**Multi-Protocol Scanning**
SMB, LDAP, MSSQL, RDP, FTP, NFS, and VNC enumeration in a single scan. Port availability is auto-detected before each module runs.

**Actionable Next Steps**
Findings generate ready-to-run commands with your credentials auto-filled. Priority-ranked with auto-exploit warnings for dangerous modules like secretsdump and ntlmrelayx.

**Zero Dependencies**
Only requires Python 3.10+ and NetExec on your PATH. No pip packages, no virtual environments, no build steps.

</td>
<td width="50%">

**Multi-Target Scanning**
CIDR ranges, IP ranges, and target files. Parallel host discovery scans /24 networks in seconds. Per-target results with aggregate summary.

**Multi-Credential Mode**
Test multiple credentials with `-C creds.txt`. Visual share access matrix, admin detection, and access comparison across users.

**Copy-Paste Output**
Clean line-by-line lists of usernames, SPNs, shares, computers, and more. Pipe directly to other tools or save to files.

**Proxy Mode**
Full proxychains/SOCKS support. Auto-reduces concurrency, increases timeouts, and skips incompatible modules. Auto-detected via `LD_PRELOAD`.

</td>
</tr>
</table>

---

## Quick Start

### Prerequisites

<table>
<tr>
<th>Requirement</th>
<th>Version</th>
<th>Purpose</th>
</tr>
<tr>
<td>Python</td>
<td>3.10+</td>
<td>Runtime</td>
</tr>
<tr>
<td>NetExec</td>
<td>Latest</td>
<td>Required (must be in PATH)</td>
</tr>
</table>

### Install

```bash
# pipx (recommended — isolated environment, global command)
pipx install git+https://github.com/Real-Fruit-Snacks/Maelstrom.git

# Or standard pip
pip install git+https://github.com/Real-Fruit-Snacks/Maelstrom.git

# Development
git clone https://github.com/Real-Fruit-Snacks/Maelstrom.git
cd maelstrom && pip install -e .
```

### Verification

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

---

## Modules

<table>
<tr>
<th>Module</th>
<th>Protocol</th>
<th>Description</th>
</tr>
<tr><td>Users</td><td>RPC</td><td>Domain users with built-in/service/domain categorization</td></tr>
<tr><td>Groups</td><td>RPC</td><td>Domain groups with high-value highlighting and members</td></tr>
<tr><td>Local Groups</td><td>RPC</td><td>Local groups and Administrators members</td></tr>
<tr><td>Computers</td><td>LDAP</td><td>Domain computers with OS info and outdated detection</td></tr>
<tr><td>Shares</td><td>SMB</td><td>Share permissions (matrix in multi-cred mode)</td></tr>
<tr><td>Spider</td><td>SMB</td><td>Recursive file listing on shares (metadata or download)</td></tr>
<tr><td>Policies</td><td>RPC</td><td>Password and lockout policies</td></tr>
<tr><td>Sessions</td><td>RPC</td><td>Active Windows sessions <code>[admin]</code></td></tr>
<tr><td>Logged On</td><td>RPC</td><td>Currently logged on users <code>[admin]</code></td></tr>
<tr><td>Printers</td><td>RPC</td><td>Print spooler status with PrintNightmare warning</td></tr>
<tr><td>AV/EDR</td><td>RPC</td><td>Installed security products <code>[admin]</code></td></tr>
<tr><td>LAPS</td><td>LDAP</td><td>LAPS deployment and password read permissions</td></tr>
<tr><td>LDAP Signing</td><td>LDAP</td><td>Signing and channel binding requirements</td></tr>
<tr><td>Pre-2K Computers</td><td>LDAP</td><td>Computers with weak default passwords</td></tr>
<tr><td>BitLocker</td><td>RPC</td><td>Drive encryption status <code>[admin]</code></td></tr>
<tr><td>Kerberoastable</td><td>LDAP</td><td>Accounts with SPNs via LDAP query</td></tr>
<tr><td>AS-REP Roastable</td><td>LDAP</td><td>Accounts without pre-authentication</td></tr>
<tr><td>Delegation</td><td>LDAP</td><td>Unconstrained/constrained/RBCD delegation</td></tr>
<tr><td>ADCS</td><td>LDAP</td><td>Certificate templates and certificate authorities</td></tr>
<tr><td>DC List</td><td>LDAP</td><td>Domain controllers and trust relationships</td></tr>
<tr><td>AdminCount</td><td>LDAP</td><td>Accounts with adminCount=1</td></tr>
<tr><td>PASSWD_NOTREQD</td><td>LDAP</td><td>Accounts without password requirement</td></tr>
<tr><td>gMSA</td><td>LDAP</td><td>Group Managed Service Account enumeration</td></tr>
<tr><td>GPP Password</td><td>SMB</td><td>Group Policy Preferences cpassword extraction (MS14-025)</td></tr>
<tr><td>PSO</td><td>LDAP</td><td>Fine-Grained Password Policies (Password Settings Objects)</td></tr>
<tr><td>SCCM</td><td>LDAP</td><td>SCCM/MECM infrastructure discovery</td></tr>
<tr><td>MAQ</td><td>LDAP</td><td>Machine Account Quota check</td></tr>
<tr><td>WebDAV</td><td>SMB</td><td>WebClient service status check</td></tr>
<tr><td>DNS</td><td>--</td><td>DNS enumeration recommendations (passive)</td></tr>
<tr><td>Descriptions</td><td>LDAP</td><td>User description fields (password hunting)</td></tr>
<tr><td>SMB Signing</td><td>SMB</td><td>SMB signing requirements</td></tr>
<tr><td>Subnets</td><td>LDAP</td><td>AD sites and network topology</td></tr>
<tr><td>Network Interfaces</td><td>SMB</td><td>Multi-homed host detection via SMB IOCTL</td></tr>
<tr><td>Disks</td><td>RPC</td><td>Disk drive enumeration <code>[admin]</code></td></tr>
<tr><td>MSSQL</td><td>MSSQL</td><td>Service detection, auth test, query recommendations</td></tr>
<tr><td>RDP</td><td>RDP</td><td>RDP status and NLA requirements</td></tr>
<tr><td>FTP</td><td>FTP</td><td>Anonymous access and credential testing</td></tr>
<tr><td>NFS</td><td>NFS</td><td>NFS exports and permissions</td></tr>
<tr><td>VNC</td><td>VNC</td><td>VNC service detection (ports 5900-5903, 5800-5801)</td></tr>
<tr><td>iOXID</td><td>DCOM</td><td>Multi-homed host discovery via DCOM (port 135)</td></tr>
</table>

---

## Architecture

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

<table>
<tr>
<th>Level</th>
<th>Workers</th>
<th>Purpose</th>
</tr>
<tr><td>Module-level</td><td>15</td><td>Independent enum modules in parallel</td></tr>
<tr><td>Target-level</td><td>5</td><td>Multiple targets scanned concurrently</td></tr>
<tr><td>Port prescan</td><td>100</td><td>Fast TCP port 445 filtering</td></tr>
<tr><td>Proxy mode</td><td>2</td><td>Reduced for SOCKS/proxychains compatibility</td></tr>
</table>

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

### Tech Stack

<table>
<tr>
<th>Layer</th>
<th>Technology</th>
</tr>
<tr><td>Language</td><td>Python 3.10+ (zero external deps)</td></tr>
<tr><td>Engine</td><td>NetExec (nxc) via subprocess</td></tr>
<tr><td>Parallelism</td><td>ThreadPoolExecutor (stdlib)</td></tr>
<tr><td>Colors</td><td>Catppuccin Mocha (24-bit true color)</td></tr>
<tr><td>Output</td><td>enum4linux-ng style indicators</td></tr>
<tr><td>Testing</td><td>pytest, unittest (249 tests)</td></tr>
<tr><td>Formatting</td><td>Black, isort, flake8</td></tr>
</table>

### Testing

```bash
pytest tests/ -v                        # All 249 tests
pytest tests/test_parsing.py -v         # Single file
pytest tests/ --cov=maelstrom           # With coverage
pytest tests/ -m "not slow"             # Skip slow tests
```

### Exit Codes

<table>
<tr>
<th>Code</th>
<th>Meaning</th>
</tr>
<tr><td><code>0</code></td><td>Success</td></tr>
<tr><td><code>1</code></td><td>General error</td></tr>
<tr><td><code>2</code></td><td>Argument error</td></tr>
<tr><td><code>3</code></td><td>NetExec not found</td></tr>
</table>

---

## Platform Support

<table>
<tr>
<th>Capability</th>
<th>Linux</th>
<th>macOS</th>
<th>Windows</th>
</tr>
<tr>
<td>Full enumeration (all modules)</td>
<td>Full</td>
<td>Full</td>
<td>Full</td>
</tr>
<tr>
<td>Multi-target scanning</td>
<td>Full</td>
<td>Full</td>
<td>Full</td>
</tr>
<tr>
<td>Multi-credential mode</td>
<td>Full</td>
<td>Full</td>
<td>Full</td>
</tr>
<tr>
<td>Proxy mode (proxychains/SOCKS)</td>
<td>Full</td>
<td>Full</td>
<td>Limited</td>
</tr>
<tr>
<td>Color output (Catppuccin Mocha)</td>
<td>Full</td>
<td>Full</td>
<td>Full (Windows Terminal)</td>
</tr>
<tr>
<td>Kerberos authentication</td>
<td>Full</td>
<td>Full</td>
<td>Full</td>
</tr>
<tr>
<td>Certificate-based auth</td>
<td>Full</td>
<td>Full</td>
<td>Full</td>
</tr>
</table>

---

## Security

### Vulnerability Reporting

**Report security issues via:**
- GitHub Security Advisories (preferred)
- Private disclosure to maintainers
- Responsible disclosure timeline (90 days)

**Do NOT:**
- Open public GitHub issues for vulnerabilities
- Disclose before coordination with maintainers

### Safety Principles

| Principle | Implementation |
|-----------|----------------|
| **Read-only** | LDAP queries, SMB enumeration, RPC calls -- never executes commands on targets |
| **No exploitation** | Kerberoasting finds SPNs via LDAP only -- does not request TGS tickets |
| **Credential safety** | Output files created with 0o600 permissions, warns on permissive cred files |
| **Recommendations only** | MSSQL tests auth only, shows SQL queries for manual execution |
| **Auto-exploit warnings** | Next steps flag commands that automatically exploit (secretsdump, ntlmrelayx) |

### What Maelstrom Does NOT Do

- **Not an exploitation tool** -- never executes commands on target systems
- **Not a credential cracker** -- identifies Kerberoastable SPNs but does not request tickets
- **Not a C2 framework** -- no implant management, lateral movement, or beaconing
- **Not a relay tool** -- identifies relay opportunities but does not perform them

---

## License

MIT License

Copyright &copy; 2026 Real-Fruit-Snacks

```
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
THE AUTHORS ARE NOT LIABLE FOR ANY DAMAGES ARISING FROM USE.
USE AT YOUR OWN RISK AND ONLY WITH PROPER AUTHORIZATION.
```

---

## Resources

- **GitHub**: [github.com/Real-Fruit-Snacks/Maelstrom](https://github.com/Real-Fruit-Snacks/Maelstrom)
- **Issues**: [Report a Bug](https://github.com/Real-Fruit-Snacks/Maelstrom/issues)
- **Security**: [SECURITY.md](SECURITY.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

<div align="center">

**Part of the Real-Fruit-Snacks water-themed security toolkit**

[Aquifer](https://github.com/Real-Fruit-Snacks/Aquifer) • [Cascade](https://github.com/Real-Fruit-Snacks/Cascade) • [Conduit](https://github.com/Real-Fruit-Snacks/Conduit) • [Deadwater](https://github.com/Real-Fruit-Snacks/Deadwater) • [Deluge](https://github.com/Real-Fruit-Snacks/Deluge) • [Depth](https://github.com/Real-Fruit-Snacks/Depth) • [Dew](https://github.com/Real-Fruit-Snacks/Dew) • [Droplet](https://github.com/Real-Fruit-Snacks/Droplet) • [Fathom](https://github.com/Real-Fruit-Snacks/Fathom) • [Flux](https://github.com/Real-Fruit-Snacks/Flux) • [Grotto](https://github.com/Real-Fruit-Snacks/Grotto) • [HydroShot](https://github.com/Real-Fruit-Snacks/HydroShot) • [Maelstrom](https://github.com/Real-Fruit-Snacks/Maelstrom) • [Rapids](https://github.com/Real-Fruit-Snacks/Rapids) • [Ripple](https://github.com/Real-Fruit-Snacks/Ripple) • [Riptide](https://github.com/Real-Fruit-Snacks/Riptide) • [Runoff](https://github.com/Real-Fruit-Snacks/Runoff) • [Seep](https://github.com/Real-Fruit-Snacks/Seep) • [Shallows](https://github.com/Real-Fruit-Snacks/Shallows) • [Siphon](https://github.com/Real-Fruit-Snacks/Siphon) • [Slipstream](https://github.com/Real-Fruit-Snacks/Slipstream) • [Spillway](https://github.com/Real-Fruit-Snacks/Spillway) • [Surge](https://github.com/Real-Fruit-Snacks/Surge) • [Tidemark](https://github.com/Real-Fruit-Snacks/Tidemark) • [Tidepool](https://github.com/Real-Fruit-Snacks/Tidepool) • [Undercurrent](https://github.com/Real-Fruit-Snacks/Undercurrent) • [Undertow](https://github.com/Real-Fruit-Snacks/Undertow) • [Vapor](https://github.com/Real-Fruit-Snacks/Vapor) • [Wellspring](https://github.com/Real-Fruit-Snacks/Wellspring) • [Whirlpool](https://github.com/Real-Fruit-Snacks/Whirlpool)

*Remember: With great power comes great responsibility.*

</div>
