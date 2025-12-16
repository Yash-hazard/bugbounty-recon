# Bug Bounty Recon Automation Script 🔍

A Python-based automation script for **bug bounty reconnaissance** that integrates
popular open-source tools to perform subdomain enumeration, live host detection,
service scanning, and vulnerability assessment.

## 🚀 Features
- Passive subdomain enumeration (Subfinder, Amass)
- Subdomain merging & deduplication
- Live host detection (httpx)
- WAF detection (wafw00f)
- Nmap service scanning
- Nuclei CVE & misconfiguration scans
- Timestamped output directories

## 🛠 Tools Used
- subfinder
- amass
- httpx
- nuclei
- nmap
- wafw00f
- feroxbuster

## 📦 Installation

```bash
git clone https://github.com/<your-username>/bugbounty-recon.git
cd bugbounty-recon

