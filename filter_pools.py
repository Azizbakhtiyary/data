import json

def filter_pools(input_file, output_file, min_apy=100):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Проверяем, есть ли ключ "data"
    if "data" not in data:
        print("Ошибка: В файле нет ключа 'data'")
        return

    filtered_pools = [
        pool for pool in data["data"] 
        if isinstance(pool, dict) and "apy" in pool and isinstance(pool["apy"], (int, float)) and pool["apy"] >= min_apy
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_pools, f, indent=4, ensure_ascii=False)

# Запускаем фильтрацию
filter_pools("pools.json", "filtered_pools.json")
