import requests
import json

URL = "https://yields.llama.fi/pools"  # Ссылка на данные

def fetch_data():
    try:
        response = requests.get(URL, timeout=10)  # Добавлен тайм-аут 10 секунд
        response.raise_for_status()  # Проверяем, нет ли ошибок HTTP

        data = response.json()

        with open("pools.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print("✅ Данные обновлены и сохранены в pools.json")

    except requests.exceptions.Timeout:
        print("❌ Ошибка: Истекло время ожидания ответа от API DefiLlama.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при запросе к API: {e}")
    except Exception as e:
        print(f"❌ Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    fetch_data()
