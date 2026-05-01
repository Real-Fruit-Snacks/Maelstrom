<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-light.svg">
  <img alt="Maelstrom" src="https://raw.githubusercontent.com/Real-Fruit-Snacks/Maelstrom/main/docs/assets/logo-dark.svg" width="100%">
</picture>

> [!IMPORTANT]
> **NetExec wrapper combining 35+ AD enumeration modules into a single command.** SMB, LDAP, MSSQL, RDP, FTP, NFS, and VNC enumeration with Catppuccin Mocha output, multi-target CIDR scanning, actionable next steps with auto-filled credentials, and proxy mode. Zero external Python dependencies.

> *A maelstrom is a violent whirlpool that pulls everything in range into its vortex. Felt fitting for a tool that sweeps through an AD environment with 35+ enumeration queries spinning in parallel — chaotic, powerful, and thorough.*

---

## §1 / Premise

Maelstrom is a **NetExec enumeration wrapper** that runs 35+ AD modules against a target in a single command. Users, groups, shares, LAPS, Kerberoastable accounts, delegation, ADCS, gMSA, GPP passwords, PSO, SCCM, computers, sessions, AV/EDR, LDAP/SMB signing — all in one pass. Run everything with `-A` or pick specific modules with individual flags across SMB, LDAP, MSSQL, RDP, FTP, NFS, and VNC.

Multi-target mode accepts CIDR ranges, IP ranges, and target files. A 100-thread port prescan discovers live SMB hosts across /24 networks in seconds. Multi-credential mode compares access levels visually — share permission matrices across users, admin detection, access comparison. The credential cache primes 7 parallel queries on first run so module execution is fast.

Findings generate ready-to-run commands with credentials auto-filled. Priority-ranked next steps flag dangerous modules (secretsdump, ntlmrelayx) with auto-exploit warnings. Proxy mode auto-detects via `LD_PRELOAD`, reduces concurrency, and skips incompatible modules for seamless proxychains operation.

**Authorization Required**: Designed exclusively for authorized security testing with explicit written permission.

---

## §2 / Specs

| KEY        | VALUE                                                                       |
|------------|-----------------------------------------------------------------------------|
| MODULES    | **35+ AD modules** · Users · Groups · Shares · LAPS · Kerberoastable · ADCS + more |
| PROTOCOLS  | **SMB · LDAP · MSSQL · RDP · FTP · NFS · VNC** · 7 protocol types          |
| TARGETS    | **CIDR + range + file** · 100-thread port prescan · per-target results       |
| OUTPUT     | **Catppuccin Mocha** · next steps · copy-paste lists · JSON · share matrix   |
| TESTS      | **249 pytest** · ThreadPoolExecutor · proxy mode · 15 workers default        |
| PLATFORM   | **Python 3.10+** · Linux · macOS · Windows · zero external Python deps       |
| STACK      | **NetExec (nxc)** · subprocess · ThreadPoolExecutor (stdlib) · Catppuccin Mocha |

Architecture in §5 below.

---

## §3 / Quickstart

```bash
# pipx (recommended)
pipx install git+https://github.com/Real-Fruit-Snacks/Maelstrom.git

# Or standard pip
pip install git+https://github.com/Real-Fruit-Snacks/Maelstrom.git
```

```bash
# Anonymous enumeration (auto-probes null/guest sessions)
maelstrom 10.0.0.1

# Single credential — full enumeration
maelstrom 10.0.0.1 -u admin -p 'Password123' -d CORP

# Pass-the-hash
maelstrom 10.0.0.1 -u admin -H aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0

# Multi-credential — compare access levels
maelstrom 10.0.0.1 -C creds.txt -d CORP

# Multi-target — CIDR, range, or file
maelstrom 10.0.0.0/24 -u admin -p 'Password123'

# Specific modules only
maelstrom 10.0.0.1 -u admin -p pass --shares --users --laps --mssql
```

Requires Python 3.10+ and NetExec on your PATH.

---

## §4 / Reference

```
TARGET AND AUTH

  TARGET               IP, hostname, CIDR, range, or target file
  -u -p -H -d          Username, password, NTLM hash, domain
  -k --use-kcache      Kerberos auth, ccache
  --aesKey             AES encryption key
  -C -U -P             Credential files with spray controls

MODULES (select or use -A for all)

  --shares             Share enumeration (matrix in multi-cred mode)
  --users              Domain users (built-in/service/domain categorized)
  --groups             Domain groups with high-value highlighting
  --laps               LAPS deployment and password read permissions
  --kerberoast         Kerberoastable accounts via LDAP query
  --asrep              AS-REP roastable accounts
  --delegation         Unconstrained/constrained/RBCD delegation
  --adcs               Certificate templates and authorities
  --gmsa               Group Managed Service Account enumeration
  --gpp                Group Policy Preferences cpassword extraction
  --pso                Fine-Grained Password Policies
  --sccm               SCCM/MECM infrastructure discovery
  --computers          Domain computers with OS, outdated detection
  --sessions           Active Windows sessions [admin]
  --avedr              Installed security products [admin]
  --mssql              MSSQL service detection and auth
  --rdp                RDP status and NLA requirements
  --ftp                FTP anonymous access and credential testing
  --nfs                NFS exports and permissions
  --vnc                VNC service detection (ports 5900-5903)
  -A                   Run all modules

OUTPUT AND BEHAVIOR

  -o -j --copy-paste   File output, JSON, copy-paste lists
  --proxy-mode         Proxychains/SOCKS support (auto-detected via LD_PRELOAD)
  --debug --timeout    Runtime behavior controls
  --discover-only      Live SMB host discovery only
```

---

## §5 / Architecture

```
maelstrom/
  maelstrom/
    cli/
      args.py               Argument parsing (70+ flags)
      main.py               Orchestration, module dispatch
    core/
      colors.py             Catppuccin Mocha terminal colors
      constants.py          Regex patterns, thread pool sizes
      output.py             Buffered output system
      parallel.py           ThreadPoolExecutor module runner
      runner.py             NetExec subprocess execution
    enums/                  35+ enumeration modules
    models/                 EnumCache, Credential, results
    parsing/                NXC output parsers
    reporting/              Summary, next steps, share matrix
    validation/             Credential and anonymous validation
  tests/                    249 pytest tests
```

| Layer        | Implementation                                                  |
|--------------|-----------------------------------------------------------------|
| **Engine**   | NetExec (nxc) via subprocess                                    |
| **Language** | Python 3.10+ · zero external Python dependencies                |
| **Parallelism** | ThreadPoolExecutor (stdlib) · 15 workers default · 2 in proxy mode |
| **Colors**   | Catppuccin Mocha · 24-bit true color                            |
| **Testing**  | pytest · 249 tests                                              |
| **Formatting** | Black · isort · flake8                                        |

Execution proceeds in phases: port prescan (100 threads), SMB validation, auth probe, cache priming (7 parallel queries), sequential domain intel, then 36 independent modules via ThreadPoolExecutor. Proxy mode auto-reduces to 2 workers and skips incompatible modules.

---

## §6 / Platform Support

| Capability | Linux | macOS | Windows |
|------------|-------|-------|---------|
| Full enumeration | Full | Full | Full |
| Multi-target scanning | Full | Full | Full |
| Multi-credential mode | Full | Full | Full |
| Proxy mode | Full | Full | Limited |
| Kerberos authentication | Full | Full | Full |
| Certificate-based auth | Full | Full | Full |

---

[License: MIT](LICENSE) · Part of [Real-Fruit-Snacks](https://github.com/Real-Fruit-Snacks) — building offensive security tools, one wave at a time.
