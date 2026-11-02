import os
import json

def update_catalog():
    # Папка, где лежит сам скрипт
    folder = os.path.dirname(os.path.abspath(__file__))
    
    # Находим все .json файлы, кроме catalog.json
    json_files = []
    for file in os.listdir(folder):
        if file.lower().endswith('.json') and file.lower() != 'catalog.json':
            json_files.append(file)
    
    # Сортируем по алфавиту (регистронезависимо)
    json_files.sort(key=lambda x: x.lower())
    
    # Формируем список
    catalog = [{"file": f} for f in json_files]
    
    # Записываем catalog.json
    catalog_path = os.path.join(folder, 'catalog.json')
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    
    print(f"✅ catalog.json обновлён. Файлов: {len(catalog)}")
    for item in catalog:
        print(f"   - {item['file']}")

if __name__ == '__main__':
    update_catalog()
    input("\nНажмите Enter для выхода...")