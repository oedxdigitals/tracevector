# TRACEVECTOR (tvx)

TRACEVECTOR is a professional, terminal-first OSINT investigation CLI designed for investigators, analysts, and security professionals.

It runs as a **single portable binary**, supports a **plugin-based architecture**, and performs ethical open-source intelligence lookups on targets such as phone numbers, IP addresses, and email addresses.

---

## Features

- 🔍 OSINT investigations from the terminal
- 🧩 Plugin-based architecture
- 📦 Single-file portable binary (PyInstaller)
- 🕵️ Phone number metadata investigation
- 🧪 Built-in self diagnostics (`tvx doctor`)
- 📄 JSON output support
- ⚙️ Works in minimal / container / Android-like environments

---

## Installation

### Option 1: Use prebuilt binary
```bash
chmod +x tvx
./tvx --version
### Option 2: Use pip
'''bash
pip instal tracevector

### v2.5.0 Help Text
TRACEVECTOR performs lawful, metadata-based OSINT only.
Private communications are never accessed.
