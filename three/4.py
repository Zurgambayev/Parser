import requests
import random
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of User Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
]

# List of Proxy Servers (if available)
PROXIES = [
    # "http://username:password@proxy_ip:proxy_port",  # Format for proxy with authentication
    # "http://proxy_ip:proxy_port",                   # Format for proxy without authentication
]

# Загрузка брендов из файла
with open('three/letter_combinations.txt', 'r') as file:
    brands = [line.strip() for line in file.readlines()]

# Базовый URL
base_url = "https://www.vinted.pl/api/v2/catalog/filters/search"

# Словарь для хранения данных и множество для проверки существующих ключей
with open('brand_map.json', 'r') as json_file:
    brand_map = json.load(json_file)
existing_ids = set(brand_map.keys())
print("Данные успешно загружены из brand_map.json")

# Function to send a single GET request
def send_request(session, brand, user_agent, proxy=None):
    headers = {
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.vinted.pl/",
        "Connection": "keep-alive"
    }
    params = {
        "filter_search_code": "brand",
        "filter_search_text": brand,
        "search_text": brand,
        "catalog_ids": "",
        "size_ids": "",
        "brand_ids": "",
        "status_ids": "",
        "color_ids": "",
        "material_ids": ""
    }
    try:
        response = session.get(base_url, params=params, headers=headers, proxies={"http": proxy, "https": proxy} if proxy else None)
        if response.status_code == 200:
            data = response.json()
            for option in data.get('options', []):
                if option['id'] in existing_ids:
                    continue
                brand_map[option['id']] = {
                    'brand': option['title']
                }
                existing_ids.add(option['id'])
                with open('brand_map2.json', 'w') as outfile:
                    json.dump(brand_map, outfile, indent=4, ensure_ascii=False)
        else:
            print(f"Ошибка при запросе для бренда {brand}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed for brand {brand}: {e}")
    return response.status_code if response else None

# Function to handle multiple requests concurrently
def send_requests_concurrently(brands, total_requests, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with requests.Session() as session:
            futures = []
            for i in range(total_requests):
                brand = brands[i % len(brands)]  # Cycles through the brands list
                user_agent = random.choice(USER_AGENTS)
                proxy = random.choice(PROXIES) if PROXIES else None

                # Schedule the request with random delay
                futures.append(executor.submit(send_request, session, brand, user_agent, proxy))
                time.sleep(random.uniform(0.1, 1))  # Reduced random delay for faster execution

            # Wait for all futures to complete
            for future in as_completed(futures):
                if future.result() is not None:
                    print(f"Request completed with status: {future.result()}")

# Main function to run the script
if __name__ == "__main__":
    TOTAL_REQUESTS = 19000  # Number of requests to send
    MAX_WORKERS = 20  # Increased number of concurrent threads for faster execution
    
    send_requests_concurrently(brands, TOTAL_REQUESTS, MAX_WORKERS)

    # Запись данных в текстовый файл
    with open('brand_map2.json', 'w') as outfile:
        json.dump(brand_map, outfile, indent=4, ensure_ascii=False)

    print("Данные успешно сохранены в файл brand_map2.json")
