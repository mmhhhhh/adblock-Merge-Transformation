import requests
import yaml

urls = [
    "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockmihomolite.yaml",
    "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-clash.yaml"
]

def download_yaml(url):
    response = requests.get(url)
    response.raise_for_status()
    data = yaml.safe_load(response.text)
    return data.get("payload", [])

all_rules = set()
raw_count = 0  # 原始规则总数量（包含重复）

for url in urls:
    rules = download_yaml(url)
    raw_count += len(rules)
    all_rules.update(rules)

deduped_count = len(all_rules)
removed_count = raw_count - deduped_count

output_data = {
    "payload": sorted(all_rules)
}

with open("adblock_reject.yaml", "w", encoding="utf-8") as f:
    yaml.dump(output_data, f, allow_unicode=True)

print(f"原始规则总数：{raw_count}")
print(f"去重后规则数：{deduped_count}")
print(f"共去重：{removed_count} 条规则")
print("已保存为 adblock_reject.yaml")
