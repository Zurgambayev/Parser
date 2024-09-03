import json

# Загрузка данных из JSON-файла
with open('brand_map.json', 'r') as file:
    data = json.load(file)

# Создание словаря (map) с id в качестве ключей
brand_map = {}

for brand_id, brand_info in data.items():
    brand_map[brand_id] = brand_info

# Вывод словаря в терминал
print(json.dumps(brand_map, indent=4, ensure_ascii=False))

# Запись словаря обратно в файл, если необходимо
with open('brand_map_output.json', 'w') as outfile:
    json.dump(brand_map, outfile, indent=4, ensure_ascii=False)

print("Данные успешно сохранены в файл brand_map_output.json")
