import json

def filter_pools(input_file, output_file, min_apy=100, min_tvl=50000):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "data" not in data:
        print("Ошибка: В файле нет ключа 'data'")
        return

    filtered_pools = []

    for pool in data["data"]:
        apy = pool.get("apy", 0)
        tvl = pool.get("tvlUsd", 0)

        if isinstance(apy, (int, float)) and isinstance(tvl, (int, float)) and apy >= min_apy and tvl >= min_tvl:
            filtered_pools.append(pool)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_pools, f, indent=4, ensure_ascii=False)

    log_message = f"✅ Фильтрация завершена: {len(filtered_pools)} пулов с APY ≥ {min_apy}% и TVL ≥ ${min_tvl}"
    print(log_message)

    with open("filter_log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(log_message)

if __name__ == "__main__":
    filter_pools("pools.json", "filtered_pools.json")
