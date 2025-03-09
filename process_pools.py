import json
import requests

def get_pool_data(pool_id):
    url = f"https://api.llama.fi/chart/{pool_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"⚠️ Пропуск пула {pool_id}: 404 Not Found")
        else:
            print(f"❌ Ошибка HTTP для пула {pool_id}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Ошибка сети для пула {pool_id}: {req_err}")
    return None

def process_pools(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            pools = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Ошибка при чтении {input_file}: {e}")
        pools = []

    valid_pools = []
    
    for pool in pools:
        pool_id = pool.get("id")
        if not pool_id:
            continue

        pool_data = get_pool_data(pool_id)
        if pool_data:
            pool["historical_data"] = pool_data
            valid_pools.append(pool)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(valid_pools, f, indent=4, ensure_ascii=False)

    with open("filter_log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(str(len(valid_pools)))

    print(f"✅ Обработано пулов: {len(valid_pools)}")

if __name__ == "__main__":
    process_pools("filtered_pools.json", "valid_pools.json")
