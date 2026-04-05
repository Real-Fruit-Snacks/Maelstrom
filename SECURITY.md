# Security Policy

## Supported Versions

Only the latest release of Maelstrom is supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < latest | :x:               |

## Reporting a Vulnerability

**Do NOT open public issues for security vulnerabilities.**

If you discover a security vulnerability in Maelstrom, please report it responsibly:

1. **Preferred:** Use [GitHub Security Advisories](https://github.com/Real-Fruit-Snacks/Maelstrom/security/advisories/new) to create a private report.
2. **Alternative:** Email the maintainers directly with details of the vulnerability.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment:** Within 48 hours of receipt
- **Assessment:** Within 7 days
- **Fix & Disclosure:** Within 90 days (coordinated responsible disclosure)

We follow a 90-day responsible disclosure timeline. If a fix is not released within 90 days, the reporter may disclose the vulnerability publicly.

## What is NOT a Vulnerability

Maelstrom is a NetExec wrapper for Active Directory enumeration. The following behaviors are **features, not bugs**:

- Executing NetExec commands against specified targets with provided credentials
- Enumerating SMB shares, users, groups, policies, and other AD objects
- Generating next-step recommendations including potentially dangerous commands
- Displaying credential information in terminal output and copy-paste lists
- Multi-target scanning across CIDR ranges and target files

These capabilities exist by design for legitimate security testing workflows. Reports that simply describe Maelstrom working as intended will be closed.

## Responsible Use

Maelstrom is intended for authorized penetration testing, security research, and educational purposes only. Users are responsible for ensuring they have proper authorization before enumerating any systems.
