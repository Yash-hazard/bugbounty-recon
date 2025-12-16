import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, label=None):
    print(f"\n[+] Running: {label or cmd}")
    subprocess.run(cmd, shell=True)

def combine_subdomain_files(directory):
    combined_file = "all_subdomains.txt"
    with open(combined_file, "w") as outfile:
        seen = set()
        for txt_file in Path(directory).rglob("*.txt"):
            with open(txt_file) as infile:
                for line in infile:
                    line = line.strip()
                    if line and line not in seen:
                        outfile.write(line + "\n")
                        seen.add(line)
    print(f"[+] Combined and deduplicated subdomains saved to {combined_file}")
    return combined_file

def recon(domain, sub_file):
    run_command(f"subfinder -d {domain} -silent -o subfinder.txt", "subfinder")
    run_command(f"amass enum -passive -d {domain} -o amass.txt", "amass")
    
    run_command(f"cat subfinder.txt amass.txt {sub_file} | sort -u > all_subdomains.txt", "Combining all subdomains")

    run_command("httpx -l all_subdomains.txt -silent -title -status-code -tech-detect -o live_subdomains.txt", "httpx")

    run_command(f"python3 photon.py -u https://{domain} -o photon_output", "photon")

    run_command("wafw00f https://" + domain, "wafw00f")

    run_command("nmap -sV -O -T4 -Pn -iL all_subdomains.txt -oA nmap_scan", "nmap")

    run_command("feroxbuster -u https://" + domain + " -w ~/rockyou.txt -t 200 -o feroxbuster.txt", "feroxbuster")

def vulnerability_scan():
    run_command("nuclei -l live_subdomains.txt -t cves/ -severity critical,high,medium -o nuclei_output.txt", "Nuclei CVEs")
    run_command("nuclei -l live_subdomains.txt -tags misconfiguration -o misconfig_output.txt", "Nuclei Misconfig")

def main():
    parser = argparse.ArgumentParser(description="Universal Bug Bounty Recon Script")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("-f", "--folder", help="Folder containing subdomain .txt files", required=True)

    args = parser.parse_args()

    combined = combine_subdomain_files(args.folder)
    recon(args.domain, combined)
    vulnerability_scan()

if __name__ == "__main__":
    main()
