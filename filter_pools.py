import json
import requests
from datetime import datetime, timedelta

def get_historical_data(pool_id):
    url = f"https://api.llama.fi/chart/{pool_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении данных для пула {pool_id}: {e}")
        return []

def calculate_average_apy_tvl(historical_data, days=7):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    filtered_data = [
        entry for entry in historical_data
        if start_date <= datetime.utcfromtimestamp(entry['date']) <= end_date
    ]
    if not filtered_data:
        return None, None
    average_apy = sum(entry['apy'] for entry in filtered_data) / len(filtered_data)
    average_tvl = sum(entry['tvlUsd'] for entry in filtered_data) / len(filtered_data)
    return average_apy, average_tvl

def filter_pools(input_file, output_file, min_apy=100, min_tvl=50000):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "data" not in data:
        print("Ошибка: В файле нет ключа 'data'")
        return

    filtered_pools = []

    for pool in data["data"]:
        pool_id = pool.get("pool")
        if not pool_id:
            continue

        historical_data = get_historical_data(pool_id)
        if not historical_data:
            continue

        avg_apy, avg_tvl = calculate_average_apy_tvl(historical_data)
        if avg_apy is None or avg_tvl is None:
            continue

        if avg_apy >= min_apy and avg_tvl >= min_tvl:
            filtered_pools.append(pool)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_pools, f, indent=4, ensure_ascii=False)

    log_message = f"✅ Фильтрация завершена: {len(filtered_pools)} пулов с средним APY ≥ {min_apy}% и средним TVL ≥ ${min_tvl} за последние 7 дней."
    print(log_message)

    with open("filter_log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(log_message)

if __name__ == "__main__":
    filter_pools("pools.json", "filtered_pools.json")
