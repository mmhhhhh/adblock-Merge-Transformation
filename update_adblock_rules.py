import requests

# 规则源
urls = [
    "https://filters.adtidy.org/android/filters/15_optimized.txt",
    "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt",
    "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
    "https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt",
    "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt"
]

output_file = "merged-adblock.txt"  # 输出文件名

def fetch_and_merge():
    rules = set()
    total_rules = 0  # 记录总规则数

    # 拉取并合并规则
    for url in urls:
        try:
            print(f"Fetching {url}")
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            lines = resp.text.splitlines()
            total_rules += len(lines)  # 累计每个文件的规则数

            for line in lines:
                line = line.strip()
                if line and not line.startswith("!") and not line.startswith("#"):
                    rules.add(line)  # 去重并合并

        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # 去重后的规则数
    deduplicated_count = len(rules)
    removed_count = total_rules - deduplicated_count  # 计算去除的规则数

    # 输出去重信息
    print(f"Total rules fetched: {total_rules}")
    print(f"Deduplicated rules: {deduplicated_count}")
    print(f"Removed rules: {removed_count}")

    # 写入去重后的规则文件
    sorted_rules = sorted(rules)
    with open(output_file, "w", encoding="utf-8") as f:
        for rule in sorted_rules:
            f.write(rule + "\n")

    print(f"Merged and deduplicated {deduplicated_count} rules into {output_file}")

if __name__ == "__main__":
    fetch_and_merge()
