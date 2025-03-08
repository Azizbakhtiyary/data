import requests
import json

URL = "https://yields.llama.fi/pools"  # Ссылка на данные

def fetch_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        with open("pools.json", "w") as f:
            json.dump(data, f, indent=4)
        print("✅ Данные обновлены и сохранены в pools.json")
    else:
        print(f"❌ Ошибка запроса: {response.status_code}")

if __name__ == "__main__":
    fetch_data()

