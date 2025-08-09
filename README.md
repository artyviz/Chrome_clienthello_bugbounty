# Chrome-Stable (N-2) uTLS Template Generator & JA3 Analyzer

## Overview

This utility produces the exact TLS handshake bytes (ClientHello) that Chrome Stable (N-2) sends, plus a self-test to prove it matches Chrome’s JA3 fingerprint.
It’s designed for developers, security researchers, and network engineers who need to:

* Compare TLS ClientHello data from custom applications (e.g., Betanet nodes) against Chrome Stable (N-2)
* Detect JA3 fingerprint mismatches that could allow deep-packet inspection (DPI) to single out traffic
* Keep TLS fingerprints in sync when Chromium releases new stable versions

**Primary Use Case:** Make traffic blend in with normal Chrome browsing patterns to avoid fingerprint-based detection.

> ⚠ **Note:** This project is for research, testing, and responsible disclosure only.

---

## Features

* **Deterministic ClientHello generation** for Chrome Stable (N-2)
* **JA3 self-test CLI** to verify fingerprint match
* **Auto-refresh** of Chromium fingerprint metadata
* **Diff reports** highlighting mismatches in cipher suites, extensions, ALPN, and groups
* **Synthetic test data** for safe offline reproduction

---

## Repository Structure

```
betanet_chrome_clienthello_analysis/
├── analysis_cli/              # Command-line interface and core analysis logic
├── chrome-metadata/           # Chrome Stable (N-2) TLS fingerprint data
├── tests/                     # Synthetic test inputs & expected outputs
├── BUG_BOUNTY_SUBMISSION.md   # Ready-to-submit bug bounty write-up
└── README.md                  # This file
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/betanet_chrome_clienthello_analysis.git
cd betanet_chrome_clienthello_analysis
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Compare a ClientHello against Chrome Stable (N-2)

```bash
python -m analysis_cli.main \
    --input tests/synthetic_clienthello.json \
    --compare chrome-metadata/n-2.json \
    --output tests/sample_report.json
```

### Example Output

```json
{
  "ja3_match": false,
  "differences": {
    "cipher_suites": {
      "missing_in_input": [4865, 4866],
      "extra_in_input": [49327]
    },
    "extensions": {
      "missing_in_input": [51],
      "extra_in_input": []
    }
  }
}
```

---

## Auto-Refresh Chrome Fingerprint

```bash
python -m analysis_cli.update_chrome_metadata
```

Fetches the latest stable Chromium TLS ClientHello and updates the local template.

---

## Bug Bounty Context

This was originally built to identify a fingerprint mismatch in Betanet node traffic, allowing it to be distinguished from Chrome browsing.
The vulnerability write-up is in `BUG_BOUNTY_SUBMISSION.md`.

---

## License

MIT License
