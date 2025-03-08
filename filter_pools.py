import json

def filter_pools(input_file, output_file, min_apy=100):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "data" not in data:
        print("Ошибка: В файле нет ключа 'data'")
        return

    filtered_pools = [
        pool for pool in data["data"]
        if isinstance(pool, dict) and isinstance(pool.get("apy"), (int, float)) and pool["apy"] >= 100:
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_pools, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    filter_pools("pools.json", "filtered_pools.json")
