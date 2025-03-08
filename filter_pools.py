import json

def filter_pools(input_file, output_file, min_apy=100):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "data" not in data:
        print("Ошибка: В файле нет ключа 'data'")
        return

    filtered_pools = []
    
    for pool in data["data"]:
        if isinstance(pool, dict) and isinstance(pool.get("apy"), (int, float)) and pool["apy"] >= min_apy:
            filtered_pools.append(pool)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_pools, f, indent=4, ensure_ascii=False)

    log_message = f"✅ Фильтрация завершена: осталось {len(filtered_pools)} пулов с APY >= {min_apy}%"
    print(log_message)

    with open("filter_log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(log_message)
if __name__ == "__main__":
    filter_pools("pools.json", "filtered_pools.json")
