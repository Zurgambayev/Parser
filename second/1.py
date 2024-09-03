import string

def generate_letter_combinations():
    # Получаем список всех букв латинского алфавита
    letters = string.ascii_lowercase
    
    # Список для хранения всех комбинаций
    combinations = []
    
    # Генерация комбинаций из одной буквы
    for letter in letters:
        combinations.append(letter)
    
    # Генерация комбинаций из двух букв
    for letter1 in letters:
        for letter2 in letters:
            combinations.append(letter1 + letter2)
    
    # Генерация комбинаций из трех букв
    for letter1 in letters:
        for letter2 in letters:
            for letter3 in letters:
                combinations.append(letter1 + letter2 + letter3)
    
    # Возвращаем список всех комбинаций
    return combinations

# Запуск генерации комбинаций
all_combinations = generate_letter_combinations()

# Сохранение комбинаций в файл
with open("letter_combinations.txt", "w") as file:
    for combination in all_combinations:
        file.write(combination + "\n")

print("Комбинации букв сохранены в файл letter_combinations.txt")
