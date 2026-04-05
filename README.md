<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-light.svg">
  <img alt="Maelstrom" src="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-dark.svg" width="520">
</picture>

![Python](https://img.shields.io/badge/language-Python-3776AB.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**NetExec wrapper combining 35+ AD enumeration modules into a single command.**

Shells out to NetExec for SMB, LDAP, MSSQL, RDP, FTP, NFS, and VNC enumeration with colored Catppuccin Mocha output, intelligent credential handling, multi-target scanning across CIDR ranges, and actionable next-step recommendations with auto-filled credentials. Zero external Python dependencies.

> **Authorization Required**: Designed exclusively for authorized security testing with explicit written permission.

</div>

---

## Quick Start

```bash
# pipx (recommended)
pipx install git+https://github.com/Real-Fruit-Snacks/Maelstrom.git

# Or standard pip
pip install git+https://github.com/Real-Fruit-Snacks/Maelstrom.git
```

```bash
# Anonymous enumeration (auto-probes null/guest sessions)
maelstrom 10.0.0.1

# Single credential -- full enumeration
maelstrom 10.0.0.1 -u admin -p 'Password123' -d CORP

# Pass-the-hash
maelstrom 10.0.0.1 -u admin -H aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0

# Multi-credential -- compare access levels
maelstrom 10.0.0.1 -C creds.txt -d CORP

# Multi-target -- CIDR, range, or file
maelstrom 10.0.0.0/24 -u admin -p 'Password123'

# Specific modules only
maelstrom 10.0.0.1 -u admin -p pass --shares --users --laps --mssql
```

Requires Python 3.10+ and NetExec on your PATH.

---

## Features

### 35+ Enumeration Modules

Users, groups, shares, LAPS, Kerberoastable, delegation, ADCS, gMSA, GPP, PSO, SCCM, and more. Run all at once with `-A` or pick specific modules with individual flags. Covers SMB, LDAP, MSSQL, RDP, FTP, NFS, and VNC protocols.

```bash
maelstrom 10.0.0.1 -u admin -p pass -A        # All modules
maelstrom 10.0.0.1 -u admin -p pass --kerberoast --delegation --adcs
```

### Multi-Target Scanning

CIDR ranges, IP ranges, and target files. Parallel host discovery scans /24 networks in seconds with 100-thread port prescan. Per-target results with aggregate summary.

```bash
maelstrom 10.0.0.0/24 -u admin -p 'Password123'
maelstrom targets.txt -u admin -p 'Password123'
maelstrom 10.0.0.0/24 --discover-only   # Live SMB hosts only
```

### Multi-Credential Mode

Test multiple credentials with `-C creds.txt`. Visual share access matrix, admin detection, and access comparison across users.

### Actionable Next Steps

Findings generate ready-to-run commands with your credentials auto-filled. Priority-ranked with auto-exploit warnings for dangerous modules like secretsdump and ntlmrelayx.

### Proxy Mode

Full proxychains/SOCKS support. Auto-reduces concurrency, increases timeouts, and skips incompatible modules. Auto-detected via `LD_PRELOAD`.

### Copy-Paste Output

Clean line-by-line lists of usernames, SPNs, shares, computers, and more. Pipe directly to other tools or save to files with `-o` or `--copy-paste`.

---

## Modules

| Module | Protocol | Description |
|--------|----------|-------------|
| Users | RPC | Domain users with built-in/service/domain categorization |
| Groups | RPC | Domain groups with high-value highlighting and members |
| Shares | SMB | Share permissions (matrix in multi-cred mode) |
| LAPS | LDAP | LAPS deployment and password read permissions |
| Kerberoastable | LDAP | Accounts with SPNs via LDAP query |
| AS-REP Roastable | LDAP | Accounts without pre-authentication |
| Delegation | LDAP | Unconstrained/constrained/RBCD delegation |
| ADCS | LDAP | Certificate templates and certificate authorities |
| gMSA | LDAP | Group Managed Service Account enumeration |
| GPP Password | SMB | Group Policy Preferences cpassword extraction |
| PSO | LDAP | Fine-Grained Password Policies |
| SCCM | LDAP | SCCM/MECM infrastructure discovery |
| Computers | LDAP | Domain computers with OS and outdated detection |
| Sessions | RPC | Active Windows sessions [admin] |
| AV/EDR | RPC | Installed security products [admin] |
| LDAP Signing | LDAP | Signing and channel binding requirements |
| SMB Signing | SMB | SMB signing requirements |
| MSSQL | MSSQL | Service detection, auth test, query recommendations |
| RDP | RDP | RDP status and NLA requirements |
| FTP | FTP | Anonymous access and credential testing |
| NFS | NFS | NFS exports and permissions |
| VNC | VNC | VNC service detection (ports 5900-5903) |

Plus: Local Groups, Spider, Policies, Logged On, Printers, BitLocker, DC List, AdminCount, PASSWD_NOTREQD, MAQ, WebDAV, DNS, Descriptions, Subnets, Network Interfaces, Disks, iOXID, and Pre-2K Computers.

---

## Architecture

```
maelstrom/
  maelstrom/
    cli/
      args.py               # Argument parsing (70+ flags)
      main.py               # Orchestration, module dispatch
    core/
      colors.py             # Catppuccin Mocha terminal colors
      constants.py          # Regex patterns, thread pool sizes
      output.py             # Buffered output system
      parallel.py           # ThreadPoolExecutor module runner
      runner.py             # NetExec subprocess execution
    enums/                  # 35+ enumeration modules
    models/                 # EnumCache, Credential, results
    parsing/                # NXC output parsers
    reporting/              # Summary, next steps, share matrix
    validation/             # Credential and anonymous validation
  tests/                    # 249 tests
```

Execution proceeds in phases: port prescan (100 threads), SMB validation, auth probe, cache priming (7 parallel queries), sequential domain intel, then 36 independent modules via ThreadPoolExecutor with 15 workers. Proxy mode reduces to 2 workers.

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ (zero external deps) |
| Engine | NetExec (nxc) via subprocess |
| Parallelism | ThreadPoolExecutor (stdlib) |
| Colors | Catppuccin Mocha (24-bit true color) |
| Testing | pytest (249 tests) |
| Formatting | Black, isort, flake8 |

---

## Command Reference

| Category | Flags | Description |
|----------|-------|-------------|
| Target | `TARGET` | IP, hostname, CIDR, range, or target file |
| Auth | `-u -p -H -d` | Username, password, NTLM hash, domain |
| Kerberos | `-k --use-kcache --aesKey` | Kerberos auth, ccache, AES keys |
| Multi-cred | `-C -U -P` | Credential files with spray controls |
| Modules | `-A --shares --users --laps` | Select specific or all modules |
| Protocols | `--mssql --rdp --ftp --nfs` | Additional protocol enumeration |
| Output | `-o -j --copy-paste` | File output, JSON, copy-paste lists |
| Behavior | `--proxy-mode --debug --timeout` | Runtime behavior controls |

---

## Platform Support

| Capability | Linux | macOS | Windows |
|------------|-------|-------|---------|
| Full enumeration | Full | Full | Full |
| Multi-target scanning | Full | Full | Full |
| Multi-credential mode | Full | Full | Full |
| Proxy mode | Full | Full | Limited |
| Kerberos authentication | Full | Full | Full |
| Certificate-based auth | Full | Full | Full |

---

## Security

Report vulnerabilities via [SECURITY.md](SECURITY.md) or GitHub Security Advisories. Do not open public issues for security concerns.

Maelstrom is a **read-only enumeration wrapper**. It does **not**:

- Execute commands on target systems
- Request Kerberos TGS tickets (identifies SPNs via LDAP only)
- Perform relay attacks (identifies opportunities only)
- Manage implants, lateral movement, or beaconing

Output files are created with 0o600 permissions. Next steps flag commands that automatically exploit (secretsdump, ntlmrelayx) with explicit warnings.

---

## License

[MIT](LICENSE) -- Copyright 2026 Real-Fruit-Snacks
