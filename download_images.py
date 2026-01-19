import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageFont
import time

# Список всех героев Dota 2 с их URL изображениями
HEROES = [
    ("Anti-Mage", "https://dota2.ru/img/heroes/anti_mage/icon.jpg"),
    ("Axe", "https://dota2.ru/img/heroes/axe/icon.jpg"),
    ("Bane", "https://dota2.ru/img/heroes/bane/icon.jpg"),
    ("Bloodseeker", "https://dota2.ru/img/heroes/bloodseeker/icon.jpg"),
    ("Crystal Maiden", "https://dota2.ru/img/heroes/crystal_maiden/icon.jpg"),
    ("Drow Ranger", "https://dota2.ru/img/heroes/drow_ranger/icon.jpg"),
    ("Earthshaker", "https://dota2.ru/img/heroes/earthshaker/icon.jpg"),
    ("Juggernaut", "https://dota2.ru/img/heroes/juggernaut/icon.jpg"),
    ("Mirana", "https://dota2.ru/img/heroes/mirana/icon.jpg"),
    ("Morphling", "https://dota2.ru/img/heroes/morphling/icon.jpg"),
    ("Shadow Fiend", "https://dota2.ru/img/heroes/shadow_fiend/icon.jpg"),
    ("Phantom Lancer", "https://dota2.ru/img/heroes/phantom_lancer/icon.jpg"),
    ("Puck", "https://dota2.ru/img/heroes/puck/icon.jpg"),
    ("Pudge", "https://dota2.ru/img/heroes/pudge/icon.jpg"),
    ("Razor", "https://dota2.ru/img/heroes/razor/icon.jpg"),
    ("Sand King", "https://dota2.ru/img/heroes/sand_king/icon.jpg"),
    ("Storm Spirit", "https://dota2.ru/img/heroes/storm_spirit/icon.jpg"),
    ("Sven", "https://dota2.ru/img/heroes/sven/icon.jpg"),
    ("Tiny", "https://dota2.ru/img/heroes/tiny/icon.jpg"),
    ("Vengeful Spirit", "https://dota2.ru/img/heroes/vengeful_spirit/icon.jpg"),
    ("Windranger", "https://dota2.ru/img/heroes/windranger/icon.jpg"),
    ("Zeus", "https://dota2.ru/img/heroes/zeus/icon.jpg"),
    ("Kunkka", "https://dota2.ru/img/heroes/kunkka/icon.jpg"),
    ("Lina", "https://dota2.ru/img/heroes/lina/icon.jpg"),
    ("Lion", "https://dota2.ru/img/heroes/lion/icon.jpg"),
    ("Shadow Shaman", "https://dota2.ru/img/heroes/shadow_shaman/icon.jpg"),
    ("Slardar", "https://dota2.ru/img/heroes/slardar/icon.jpg"),
    ("Tidehunter", "https://dota2.ru/img/heroes/tidehunter/icon.jpg"),
    ("Witch Doctor", "https://dota2.ru/img/heroes/witch_doctor/icon.jpg"),
    ("Riki", "https://dota2.ru/img/heroes/riki/icon.jpg"),
    ("Enigma", "https://dota2.ru/img/heroes/enigma/icon.jpg"),
    ("Tinker", "https://dota2.ru/img/heroes/tinker/icon.jpg"),
    ("Sniper", "https://dota2.ru/img/heroes/sniper/icon.jpg"),
    ("Necrophos", "https://dota2.ru/img/heroes/necrophos/icon.jpg"),
    ("Warlock", "https://dota2.ru/img/heroes/warlock/icon.jpg"),
    ("Beastmaster", "https://dota2.ru/img/heroes/beastmaster/icon.jpg"),
    ("Queen of Pain", "https://dota2.ru/img/heroes/queen_of_pain/icon.jpg"),
    ("Venomancer", "https://dota2.ru/img/heroes/venomancer/icon.jpg"),
    ("Faceless Void", "https://dota2.ru/img/heroes/faceless_void/icon.jpg"),
    ("Wraith King", "https://dota2.ru/img/heroes/wraith_king/icon.jpg"),
    ("Death Prophet", "https://dota2.ru/img/heroes/death_prophet/icon.jpg"),
    ("Phantom Assassin", "https://dota2.ru/img/heroes/phantom_assassin/icon.jpg"),
    ("Pugna", "https://dota2.ru/img/heroes/pugna/icon.jpg"),
    ("Templar Assassin", "https://dota2.ru/img/heroes/templar_assassin/icon.jpg"),
    ("Viper", "https://dota2.ru/img/heroes/viper/icon.jpg"),
    ("Luna", "https://dota2.ru/img/heroes/luna/icon.jpg"),
    ("Dragon Knight", "https://dota2.ru/img/heroes/dragon_knight/icon.jpg"),
    ("Dazzle", "https://dota2.ru/img/heroes/dazzle/icon.jpg"),
    ("Clockwerk", "https://dota2.ru/img/heroes/clockwerk/icon.jpg"),
    ("Leshrac", "https://dota2.ru/img/heroes/leshrac/icon.jpg"),
    ("Nature's Prophet", "https://dota2.ru/img/heroes/natures_prophet/icon.jpg"),
    ("Lifestealer", "https://dota2.ru/img/heroes/lifestealer/icon.jpg"),
    ("Dark Seer", "https://dota2.ru/img/heroes/dark_seer/icon.jpg"),
    ("Clinkz", "https://dota2.ru/img/heroes/clinkz/icon.jpg"),
    ("Omniknight", "https://dota2.ru/img/heroes/omniknight/icon.jpg"),
    ("Enchantress", "https://dota2.ru/img/heroes/enchantress/icon.jpg"),
    ("Huskar", "https://dota2.ru/img/heroes/huskar/icon.jpg"),
    ("Night Stalker", "https://dota2.ru/img/heroes/night_stalker/icon.jpg"),
    ("Broodmother", "https://dota2.ru/img/heroes/broodmother/icon.jpg"),
    ("Bounty Hunter", "https://dota2.ru/img/heroes/bounty_hunter/icon.jpg"),
    ("Weaver", "https://dota2.ru/img/heroes/weaver/icon.jpg"),
    ("Jakiro", "https://dota2.ru/img/heroes/jakiro/icon.jpg"),
    ("Batrider", "https://dota2.ru/img/heroes/batrider/icon.jpg"),
    ("Chen", "https://dota2.ru/img/heroes/chen/icon.jpg"),
    ("Spectre", "https://dota2.ru/img/heroes/spectre/icon.jpg"),
    ("Ancient Apparition", "https://dota2.ru/img/heroes/ancient_apparition/icon.jpg"),
    ("Doom", "https://dota2.ru/img/heroes/doom/icon.jpg"),
    ("Ursa", "https://dota2.ru/img/heroes/ursa/icon.jpg"),
    ("Spirit Breaker", "https://dota2.ru/img/heroes/spirit_breaker/icon.jpg"),
    ("Gyrocopter", "https://dota2.ru/img/heroes/gyrocopter/icon.jpg"),
    ("Alchemist", "https://dota2.ru/img/heroes/alchemist/icon.jpg"),
    ("Invoker", "https://dota2.ru/img/heroes/invoker/icon.jpg"),
    ("Silencer", "https://dota2.ru/img/heroes/silencer/icon.jpg"),
    ("Outworld Destroyer", "https://dota2.ru/img/heroes/outworld_destroyer/icon.jpg"),
    ("Lycan", "https://dota2.ru/img/heroes/lycan/icon.jpg"),
    ("Brewmaster", "https://dota2.ru/img/heroes/brewmaster/icon.jpg"),
    ("Shadow Demon", "https://dota2.ru/img/heroes/shadow_demon/icon.jpg"),
    ("Lone Druid", "https://dota2.ru/img/heroes/lone_druid/icon.jpg"),
    ("Chaos Knight", "https://dota2.ru/img/heroes/chaos_knight/icon.jpg"),
    ("Meepo", "https://dota2.ru/img/heroes/meepo/icon.jpg"),
    ("Treant Protector", "https://dota2.ru/img/heroes/treant_protector/icon.jpg"),
    ("Ogre Magi", "https://dota2.ru/img/heroes/ogre_magi/icon.jpg"),
    ("Undying", "https://dota2.ru/img/heroes/undying/icon.jpg"),
    ("Rubick", "https://dota2.ru/img/heroes/rubick/icon.jpg"),
    ("Disruptor", "https://dota2.ru/img/heroes/disruptor/icon.jpg"),
    ("Nyx Assassin", "https://dota2.ru/img/heroes/nyx_assassin/icon.jpg"),
    ("Naga Siren", "https://dota2.ru/img/heroes/naga_siren/icon.jpg"),
    ("Keeper of the Light", "https://dota2.ru/img/heroes/keeper_of_the_light/icon.jpg"),
    ("Io", "https://dota2.ru/img/heroes/io/icon.jpg"),
    ("Visage", "https://dota2.ru/img/heroes/visage/icon.jpg"),
    ("Slark", "https://dota2.ru/img/heroes/slark/icon.jpg"),
    ("Medusa", "https://dota2.ru/img/heroes/medusa/icon.jpg"),
    ("Troll Warlord", "https://dota2.ru/img/heroes/troll_warlord/icon.jpg"),
    ("Centaur Warrunner", "https://dota2.ru/img/heroes/centaur_warrunner/icon.jpg"),
    ("Magnus", "https://dota2.ru/img/heroes/magnus/icon.jpg"),
    ("Timbersaw", "https://dota2.ru/img/heroes/timbersaw/icon.jpg"),
    ("Bristleback", "https://dota2.ru/img/heroes/bristleback/icon.jpg"),
    ("Tusk", "https://dota2.ru/img/heroes/tusk/icon.jpg"),
    ("Skywrath Mage", "https://dota2.ru/img/heroes/skywrath_mage/icon.jpg"),
    ("Abaddon", "https://dota2.ru/img/heroes/abaddon/icon.jpg"),
    ("Elder Titan", "https://dota2.ru/img/heroes/elder_titan/icon.jpg"),
    ("Legion Commander", "https://dota2.ru/img/heroes/legion_commander/icon.jpg"),
    ("Techies", "https://dota2.ru/img/heroes/techies/icon.jpg"),
    ("Ember Spirit", "https://dota2.ru/img/heroes/ember_spirit/icon.jpg"),
    ("Earth Spirit", "https://dota2.ru/img/heroes/earth_spirit/icon.jpg"),
    ("Underlord", "https://dota2.ru/img/heroes/underlord/icon.jpg"),
    ("Terrorblade", "https://dota2.ru/img/heroes/terrorblade/icon.jpg"),
    ("Phoenix", "https://dota2.ru/img/heroes/phoenix/icon.jpg"),
    ("Oracle", "https://dota2.ru/img/heroes/oracle/icon.jpg"),
    ("Winter Wyvern", "https://dota2.ru/img/heroes/winter_wyvern/icon.jpg"),
    ("Arc Warden", "https://dota2.ru/img/heroes/arc_warden/icon.jpg"),
    ("Monkey King", "https://dota2.ru/img/heroes/monkey_king/icon.jpg"),
    ("Dark Willow", "https://dota2.ru/img/heroes/dark_willow/icon.jpg"),
    ("Pangolier", "https://dota2.ru/img/heroes/pangolier/icon.jpg"),
    ("Grimstroke", "https://dota2.ru/img/heroes/grimstroke/icon.jpg"),
    ("Hoodwink", "https://dota2.ru/img/heroes/hoodwink/icon.jpg"),
    ("Void Spirit", "https://dota2.ru/img/heroes/void_spirit/icon.jpg"),
    ("Snapfire", "https://dota2.ru/img/heroes/snapfire/icon.jpg"),
    ("Mars", "https://dota2.ru/img/heroes/mars/icon.jpg"),
    ("Dawnbreaker", "https://dota2.ru/img/heroes/dawnbreaker/icon.jpg"),
    ("Marci", "https://dota2.ru/img/heroes/marci/icon.jpg"),
    ("Primal Beast", "https://dota2.ru/img/heroes/primal_beast/icon.jpg"),
    ("Muerta", "https://dota2.ru/img/heroes/muerta/icon.jpg")
]

def create_directory_structure():
    """Создает необходимые директории"""
    directories = [
        'static/images/heroes',
        'static/images/items',
        'static/images/default'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Создана директория: {directory}")

def create_fallback_image():
    """Создает дефолтное изображение если загрузка не удалась"""
    try:
        # Создаем изображение 256x256
        img = Image.new('RGB', (256, 256), color='#1a1a2e')
        d = ImageDraw.Draw(img)
        
        # Добавляем текст (если есть шрифты)
        try:
            # Пытаемся использовать системный шрифт
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Рисуем рамку
        d.rectangle([10, 10, 246, 246], outline='#4ecdc4', width=3)
        
        # Добавляем текст
        text = "No Image"
        text_bbox = d.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((256 - text_width) // 2, (256 - text_height) // 2)
        d.text(position, text, fill='#ffffff', font=font)
        
        # Сохраняем
        filepath = 'static/images/default/default_hero.jpg'
        img.save(filepath, 'JPEG', quality=90)
        print(f"✓ Создано дефолтное изображение: {filepath}")
        return filepath
    except Exception as e:
        print(f"✗ Ошибка создания дефолтного изображения: {str(e)}")
        return None

def normalize_filename(name):
    """Нормализует имя файла для сохранения"""
    # Заменяем недопустимые символы
    filename = name.lower()
    filename = filename.replace(' ', '_')
    filename = filename.replace("'", "")
    filename = filename.replace("-", "_")
    filename = filename.replace(".", "")
    filename = filename.replace(":", "")
    filename = filename.replace("/", "_")
    filename = filename.replace("\\", "_")
    filename = filename.replace("*", "")
    filename = filename.replace("?", "")
    filename = filename.replace("\"", "")
    filename = filename.replace("<", "")
    filename = filename.replace(">", "")
    filename = filename.replace("|", "")
    return filename + ".jpg"

def download_image(url, timeout=15):
    """Загружает одно изображение"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"  Ошибка загрузки: {str(e)}")
        return None

def download_and_save_hero(hero_data):
    """Загружает и сохраняет изображение одного героя"""
    name, url = hero_data
    filename = normalize_filename(name)
    filepath = f'static/images/heroes/{filename}'
    
    # Пропускаем если файл уже существует
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        if file_size > 1024:  # файл больше 1KB
            return name, f"/static/images/heroes/{filename}", True
        else:
            print(f"⚠ Файл {filename} слишком маленький, перезагружаю...")
    
    print(f"📥 Загружаю: {name}")
    
    # Пытаемся загрузить с основной ссылки
    image_data = download_image(url)
    
    if not image_data:
        # Если не удалось, пробуем альтернативный источник
        alt_url = url.replace("dota2.ru", "cdn.cloudflare.steamstatic.com")
        image_data = download_image(alt_url)
    
    if image_data:
        try:
            # Сохраняем изображение
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            # Проверяем размер файла
            file_size = os.path.getsize(filepath)
            if file_size < 1024:  # меньше 1KB
                print(f"  ⚠ Файл слишком маленький ({file_size} байт), возможно ошибка")
                os.remove(filepath)
                return name, "/static/images/default/default_hero.jpg", False
            
            print(f"  ✓ Сохранено: {filename} ({file_size // 1024} KB)")
            return name, f"/static/images/heroes/{filename}", True
        except Exception as e:
            print(f"  ✗ Ошибка сохранения: {str(e)}")
    else:
        print(f"  ✗ Не удалось загрузить изображение для {name}")
    
    return name, "/static/images/default/default_hero.jpg", False

def download_hero_images_parallel(max_workers=10):
    """Загружает изображения героев параллельно"""
    print("🚀 Начинаю параллельную загрузку изображений героев...")
    print(f"📊 Всего героев: {len(HEROES)}")
    print("=" * 50)
    
    results = {}
    successful = 0
    failed = 0
    skipped = 0
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Отправляем все задачи на выполнение
        future_to_hero = {executor.submit(download_and_save_hero, hero): hero for hero in HEROES}
        
        # Обрабатываем результаты по мере завершения
        for i, future in enumerate(as_completed(future_to_hero), 1):
            name, url, status = future.result()
            results[name] = url
            
            if status:
                if "default" in url:
                    failed += 1
                else:
                    successful += 1
            else:
                failed += 1
            
            # Выводим прогресс
            progress = (i / len(HEROES)) * 100
            print(f"\r📈 Прогресс: {i}/{len(HEROES)} ({progress:.1f}%) | ✓ {successful} | ✗ {failed} | ⏭ {skipped}", end="")
    
    end_time = time.time()
    
    print(f"\n" + "=" * 50)
    print(f"✅ Загрузка завершена за {end_time - start_time:.1f} секунд")
    print(f"📊 Результаты:")
    print(f"   ✓ Успешно: {successful}")
    print(f"   ✗ Не удалось: {failed}")
    print(f"   ⏭ Пропущено: {skipped}")
    
    return results

def create_update_script(results):
    """Создает скрипт для обновления базы данных"""
    script_content = '''import sqlite3

def update_hero_images():
    """Обновляет пути к изображениям в базе данных"""
    conn = sqlite3.connect('Doza.db')
    cursor = conn.cursor()
    
    hero_paths = {
'''
    
    for hero_name, image_path in sorted(results.items()):
        script_content += f'        "{hero_name}": "{image_path}",\n'
    
    script_content += '''    }
    
    for hero_name, image_path in hero_paths.items():
        cursor.execute(
            "UPDATE heroes SET image_url = ? WHERE name = ?",
            (image_path, hero_name)
        )
        print(f"Обновлено: {hero_name} -> {image_path}")
    
    conn.commit()
    conn.close()
    print(f"✅ Обновлено {len(hero_paths)} записей в базе данных")

if __name__ == "__main__":
    update_hero_images()
'''
    
    with open('update_hero_images.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n📝 Создан скрипт для обновления базы данных: update_hero_images.py")

def generate_db_init_update():
    """Генерирует обновленный список героев для db_init.py"""
    updated_heroes = []
    for hero_name, _ in HEROES:
        filename = normalize_filename(hero_name)
        image_path = f"/static/images/heroes/{filename}"
        updated_heroes.append((hero_name, image_path))
    
    # Форматируем для вставки в db_init.py
    formatted = "heroes = [\n"
    for i, (hero_name, image_path) in enumerate(updated_heroes):
        if i == len(updated_heroes) - 1:
            formatted += f'    ("{hero_name}", "{image_path}")\n'
        else:
            formatted += f'    ("{hero_name}", "{image_path}"),\n'
    formatted += "]"
    
    with open('heroes_list_for_db_init.txt', 'w', encoding='utf-8') as f:
        f.write(formatted)
    
    print(f"\n📄 Создан файл со списком героев: heroes_list_for_db_init.txt")
    print("📋 Скопируйте содержимое этого файла в функцию populate_db() в db_init.py")

def main():
    """Основная функция"""
    print("🎮 Dota 2 Hero Images Downloader")
    print("=" * 50)
    
    # Создаем структуру директорий
    create_directory_structure()
    
    # Создаем дефолтное изображение
    default_path = create_fallback_image()
    if not default_path:
        print("⚠ Предупреждение: не удалось создать дефолтное изображение")
    
    # Загружаем изображения
    results = download_hero_images_parallel(max_workers=15)
    
    # Создаем скрипт для обновления базы данных
    create_update_script(results)
    
    # Генерируем обновление для db_init.py
    generate_db_init_update()
    
    print("\n" + "=" * 50)
    print("🎉 Все готово! Далее выполните следующие шаги:")
    print("1. Запустите скрипт: python update_hero_images.py")
    print("2. Обновите db_init.py используя heroes_list_for_db_init.txt")
    print("3. Пересоздайте базу данных: python db_init.py")
    print("=" * 50)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹ Загрузка прервана пользователем")
    except Exception as e:
        print(f"\n\n💥 Критическая ошибка: {str(e)}")
