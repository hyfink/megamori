import json
import requests

# Step 1: Fetch the TXT rules from the URL
url = "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt"
response = requests.get(url)

# Initialize the rules dictionary for JSON and the content list for module
rules = {
    "version": 1,
    "rules": [
        {
            "domain": [],
            "domain_suffix": []
        }
    ]
}
module_content = []

# Step 2: Parse the fetched TXT file
if response.status_code == 200:
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("||"):
            domain = line[2:].rstrip("^")
            # For JSON
            rules["rules"][0]["domain"].append(domain)
            rules["rules"][0]["domain_suffix"].append(f".{domain}")
            # For module format (without REJECT and changed to .list)
            module_content.append(f"DOMAIN-SUFFIX,{domain}")

# Step 3: Write to a JSON file
with open("megamori.json", "w") as json_file:
    json.dump(rules, json_file, indent=4)

# Step 4: Write to a module file with DOMAIN-SUFFIX,domain format and .list extension
with open("megamori.list", "w") as module_file:
    module_file.write("\n".join(module_content))

print("Conversion completed. Both megamori.json and megamori.list files have been generated.")
