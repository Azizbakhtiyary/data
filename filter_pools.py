import json

def filter_pools(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    filtered_pools = []
    
    for pool in data:
        try:
            apy = float(pool.get("apy", 0))
            tvl = float(pool.get("tvl", 0))
            tokens = pool.get("tokens", [])
            
            if apy >= 30 and tvl > 50000 and tokens:
                filtered_pools.append(pool)
        except (ValueError, TypeError):
            continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_pools, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    filter_pools("pools.json", "filtered_pools.json")
