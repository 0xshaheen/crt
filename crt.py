import requests
import json
import sys
import os

# Banner
def print_banner():
    banner = """
    ============================================
            CRT.SH Subdomain Finder
    ============================================
    Author: 0xShaheen
    Facebook: https://facebook.com/0xshaheen
    Twitter:  https://x.com/0xshaheen
    Github:   https://github.com/0xshaheen
    LinkedIn: https://www.linkedin.com/in/0xshaheen
    Medium:   https://medium.com/@0xshaheen
    ============================================
    """
    print(banner)

# Function to fetch subdomains from crt.sh
def fetch_crtsh_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            print(f"[ERROR] Failed to parse JSON response for {domain}.")
            return

        # Extract subdomains and remove wildcard entries (*.example.com -> example.com)
        subdomains = sorted(set(entry["name_value"].replace("*.","") for entry in data if "name_value" in entry))

        if subdomains:
            output_file = f"crtsh_subs_{domain}.txt"
            with open(output_file, "w") as f:
                f.write("\n".join(subdomains))
            print(f"[+] {len(subdomains)} subdomains for {domain} saved to {output_file}")
        else:
            print(f"[!] No subdomains found for {domain}.")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch data for {domain}: {e}")

# Main function
def main():
    print_banner()

    if len(sys.argv) < 2:
        domain_or_file = input("Enter a domain (e.g., domain.com) or a file containing domains: ").strip()
    else:
        domain_or_file = sys.argv[1].strip()

    # Check if input is a file
    if os.path.isfile(domain_or_file):
        with open(domain_or_file, "r") as file:
            domains = [line.strip() for line in file if line.strip()]
        
        print(f"[+] Found {len(domains)} domains in {domain_or_file}. Fetching subdomains...\n")
        for domain in domains:
            fetch_crtsh_subdomains(domain)
    else:
        fetch_crtsh_subdomains(domain_or_file)

if __name__ == "__main__":
    main()
