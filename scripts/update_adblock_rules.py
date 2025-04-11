import requests
import hashlib
import yaml
from pathlib import Path

URLS = [
    "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-surge.txt",
    "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockclashlite.list",
    "https://raw.githubusercontent.com/Cats-Team/AdRules/main/adrules.list"
]

OUTPUT_LIST_FILE = Path("adblock_reject.list")
OUTPUT_YAML_FILE = Path("adblock_reject.yaml")

def download_rules(urls):
    all_rules = []
    for url in urls:
        try:
            print(f"Downloading: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            lines = response.text.splitlines()
            all_rules.extend([line.strip() for line in lines if line.strip() and not line.strip().startswith("#")])
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
    return all_rules

def save_if_changed(new_content, filepath):
    new_text = "\n".join(new_content) + "\n"
    if filepath.exists():
        old_text = filepath.read_text()
        if hashlib.sha256(old_text.encode()) == hashlib.sha256(new_text.encode()):
            print(f"No change in {filepath.name}. Skipping write.")
            return False
    filepath.write_text(new_text)
    print(f"Updated {filepath.name} with {len(new_content)} rules.")
    return True

def generate_yaml(rules):
    yaml_data = {
        "payload": rules
    }
    return yaml.dump(yaml_data, allow_unicode=True)

def save_yaml_if_changed(rules, filepath):
    yaml_text = generate_yaml(rules)
    if filepath.exists():
        old_text = filepath.read_text()
        if hashlib.sha256(old_text.encode()) == hashlib.sha256(yaml_text.encode()):
            print(f"No change in {filepath.name}. Skipping write.")
            return False
    filepath.write_text(yaml_text)
    print(f"Updated {filepath.name} with {len(rules)} rules.")
    return True

def main():
    rules = download_rules(URLS)
    original_count = len(rules)
    unique_rules = sorted(set(rules))
    deduplicated_count = len(unique_rules)
    print(f"Merged {original_count} rules, removed {original_count - deduplicated_count} duplicates.")
    
    save_if_changed(unique_rules, OUTPUT_LIST_FILE)
    save_yaml_if_changed(unique_rules, OUTPUT_YAML_FILE)

if __name__ == "__main__":
    main()
