import os
import json
import re

def transliterate_cyrillic(text):
    """Транслитерация кириллицы в латиницу"""
    cyrillic_to_latin = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    
    result = ''
    for char in text:
        result += cyrillic_to_latin.get(char, char)
    
    return result

def sanitize_filename(filename):
    """Убираем лишние символы из имени файла"""
    # Транслитерируем
    name = transliterate_cyrillic(filename)
    
    # Заменяем пробелы и спецсимволы на подчеркивания
    name = re.sub(r'[^\w\.\-]', '_', name)
    
    # Убираем множественные подчеркивания
    name = re.sub(r'_+', '_', name)
    
    # Убираем подчеркивания в начале и конце
    name = name.strip('_')
    
    return name

def update_catalog():
    folder = os.path.dirname(os.path.abspath(__file__))
    
    # Читаем старый catalog.json если есть
    old_catalog = {}
    catalog_path = os.path.join(folder, 'catalog.json')
    if os.path.exists(catalog_path):
        with open(catalog_path, 'r', encoding='utf-8') as f:
            old_catalog = {item['file']: item for item in json.load(f)}
    
    # Находим все .json файлы
    json_files = []
    for file in os.listdir(folder):
        if file.lower().endswith('.json') and file.lower() != 'catalog.json':
            json_files.append(file)
    
    # Переименовываем файлы
    renamed_files = []
    for old_name in json_files:
        # Проверяем, есть ли кириллица
        if re.search('[а-яА-ЯёЁ]', old_name):
            base, ext = os.path.splitext(old_name)
            new_base = sanitize_filename(base)
            new_name = new_base + ext
            
            # Если имя изменилось
            if new_name != old_name:
                old_path = os.path.join(folder, old_name)
                new_path = os.path.join(folder, new_name)
                
                # Проверяем, не существует ли уже файл с таким именем
                counter = 1
                while os.path.exists(new_path):
                    base_counter = new_base + '_' + str(counter)
                    new_name = base_counter + ext
                    new_path = os.path.join(folder, new_name)
                    counter += 1
                
                # Переименовываем
                os.rename(old_path, new_path)
                print(f"📝 {old_name} → {new_name}")
                renamed_files.append((old_name, new_name))
            else:
                renamed_files.append((old_name, old_name))
        else:
            # Файл уже на латинице
            renamed_files.append((old_name, old_name))
    
    # Сортируем по алфавиту
    renamed_files.sort(key=lambda x: x[1].lower())
    
    # Создаем новый catalog
    catalog = [{"file": new_name} for old_name, new_name in renamed_files]
    
    # Записываем catalog.json
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ catalog.json обновлён. Всего файлов: {len(catalog)}")
    print(f"🔄 Переименовано файлов: {len([f for f in renamed_files if f[0] != f[1]])}")

if __name__ == '__main__':
    print("🚀 Переименование файлов с кириллицы на латиницу...\n")
    update_catalog()
    input("\nНажмите Enter для выхода...")