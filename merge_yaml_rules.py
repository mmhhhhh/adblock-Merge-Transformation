import requests
import yaml
import hashlib

urls = [
    "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-clash.yaml",
    "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockmihomolite.yaml"
]

def download_yaml(url):
    response = requests.get(url)
    response.raise_for_status()
    data = yaml.safe_load(response.text)
    return data.get("payload", [])

all_rules = set()
for url in urls:
    rules = download_yaml(url)
    all_rules.update(rules)

output_data = {
    "payload": sorted(all_rules)
}

with open("adblock_reject.yaml", "w", encoding="utf-8") as f:
    yaml.dump(output_data, f, allow_unicode=True)

print(f"合并完成，去重后共 {len(all_rules)} 条规则，已保存为 adblock_reject.yaml")
