from flask import Flask, render_template, request, jsonify, url_for
import random
import sqlite3
import os

app = Flask(__name__)

# Имя базы данных
DB_NAME = 'Doza.db'

# Проверяем существование базы данных
def check_db_exists():
    """Проверка существования базы данных"""
    if not os.path.exists(DB_NAME):
        print(f"ОШИБКА: База данных {DB_NAME} не найдена!")
        print("Сначала запустите db_init.py для создания базы данных.")
        return False
    return True

def get_random_hero():
    """Получить случайного героя из базы данных"""
    if not check_db_exists():
        return {'name': "Unknown Hero", 'image_url': url_for('static', filename='images/placeholder.jpg')}
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, image_path FROM heroes ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    
    if result:
        image_path = result[1] if result[1] else "static/images/placeholder.jpg"
        # Преобразуем путь в URL для Flask
        if image_path.startswith('static/'):
            image_url = url_for('static', filename=image_path[7:])
        else:
            image_url = url_for('static', filename='images/placeholder.jpg')
        
        return {'name': result[0], 'image_url': image_url, 'image_path': image_path}
    return {'name': "Unknown Hero", 'image_url': url_for('static', filename='images/placeholder.jpg')}

def get_hero_by_name(hero_name):
    """Получить героя по имени"""
    if not check_db_exists():
        return None
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, image_path FROM heroes WHERE name = ?', (hero_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        image_path = result[1] if result[1] else "static/images/placeholder.jpg"
        # Преобразуем путь в URL для Flask
        if image_path.startswith('static/'):
            image_url = url_for('static', filename=image_path[7:])
        else:
            image_url = url_for('static', filename='images/placeholder.jpg')
        
        return {
            'name': result[0], 
            'image_url': image_url,
            'image_path': image_path
        }
    return None

def get_all_heroes():
    """Получить всех героев с изображениями"""
    if not check_db_exists():
        return []
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, image_path FROM heroes ORDER BY name')
    heroes = cursor.fetchall()
    conn.close()
    
    # Возвращаем список словарей с именем и изображением
    hero_list = []
    for hero in heroes:
        image_path = hero[1] if hero[1] else "static/images/placeholder.jpg"
        # Преобразуем путь в URL для Flask
        if image_path.startswith('static/'):
            image_url = url_for('static', filename=image_path[7:])
        else:
            image_url = url_for('static', filename='images/placeholder.jpg')
        
        hero_list.append({
            'name': hero[0], 
            'image_url': image_url,
            'image_path': image_path
        })
    
    return hero_list

def get_random_lane():
    """Получить случайную линию из базы данных"""
    if not check_db_exists():
        return "Random Lane"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM lanes ORDER BY RANDOM() LIMIT 1')
    lane = cursor.fetchone()[0]
    conn.close()
    return lane

def get_random_skill_build():
    """Получить случайную стратегию прокачки из базы данных"""
    if not check_db_exists():
        return "Maximize core abilities"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT type, description FROM skill_builds ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result[1]  # Возвращаем описание

def get_random_items(category, limit):
    """Получить случайные предметы определенной категории"""
    if not check_db_exists():
        return ["Item 1", "Item 2", "Item 3"][:limit]
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM items WHERE category = ? ORDER BY RANDOM() LIMIT ?', (category, limit))
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items

def generate_random_build(hero_name=None):
    """Генерация случайного билда с использованием данных из базы данных"""
    if hero_name:
        hero = get_hero_by_name(hero_name)
        if not hero:
            # Если герой не найден, берем случайного
            hero = get_random_hero()
    else:
        hero = get_random_hero()
    
    lane = get_random_lane()
    skill_build = get_random_skill_build()
    
    # Генерация предметов
    starting_items = get_random_items("starting", 6)
    early_items = get_random_items("early", 3)
    core_items = get_random_items("core", 3)
    late_items = get_random_items("late", 2)
    neutral_items = get_random_items("neutral", 2)
    
    build = {
        "hero": hero['name'],
        "hero_image": hero['image_url'],  # Используем URL, сгенерированный Flask
        "hero_image_path": hero.get('image_path', ''),  # Сохраняем путь
        "lane": lane,
        "skill_build": skill_build,
        "starting_items": starting_items,
        "early_game": early_items,
        "core_items": core_items,
        "late_game": late_items,
        "neutral_items": neutral_items
    }
    
    return build

def get_predefined_builds(hero_name=None):
    """Получить готовые билды, опционально для конкретного героя"""
    if not check_db_exists():
        return []
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if hero_name:
        cursor.execute('''
            SELECT * FROM predefined_builds 
            WHERE hero_name = ? 
            ORDER BY RANDOM() 
            LIMIT 5
        ''', (hero_name,))
    else:
        cursor.execute('SELECT * FROM predefined_builds ORDER BY RANDOM() LIMIT 5')
    
    builds = []
    for row in cursor.fetchall():
        build = {
            'id': row[0],
            'hero': row[1],
            'lane': row[2],
            'skill_build': row[3],
            'starting_items': row[4].split(',') if row[4] else [],
            'early_game': row[5].split(',') if row[5] else [],
            'core_items': row[6].split(',') if row[6] else [],
            'late_game': row[7].split(',') if row[7] else [],
            'neutral_items': row[8].split(',') if row[8] else []
        }
        
        # Получаем изображение героя
        hero = get_hero_by_name(build['hero'])
        if hero:
            build['hero_image'] = hero['image_url']
            build['hero_image_path'] = hero.get('image_path', '')
        else:
            build['hero_image'] = url_for('static', filename='images/placeholder.jpg')
            build['hero_image_path'] = "static/images/placeholder.jpg"
        
        builds.append(build)
    
    conn.close()
    return builds

def get_predefined_build_by_id(build_id):
    """Получить готовый билд по ID"""
    if not check_db_exists():
        return None
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM predefined_builds WHERE id = ?', (build_id,))
    row = cursor.fetchone()
    
    if row:
        build = {
            'id': row[0],
            'hero': row[1],
            'lane': row[2],
            'skill_build': row[3],
            'starting_items': row[4].split(',') if row[4] else [],
            'early_game': row[5].split(',') if row[5] else [],
            'core_items': row[6].split(',') if row[6] else [],
            'late_game': row[7].split(',') if row[7] else [],
            'neutral_items': row[8].split(',') if row[8] else []
        }
        
        # Получаем изображение героя
        hero = get_hero_by_name(build['hero'])
        if hero:
            build['hero_image'] = hero['image_url']
            build['hero_image_path'] = hero.get('image_path', '')
        else:
            build['hero_image'] = url_for('static', filename='images/placeholder.jpg')
            build['hero_image_path'] = "static/images/placeholder.jpg"
        
        conn.close()
        return build
    
    conn.close()
    return None

# Маршруты приложения
@app.route('/')
def index():
    heroes = get_all_heroes()
    return render_template('index.html', heroes=heroes)

@app.route('/generate')
def generate_build():
    hero_name = request.args.get('hero')
    build = generate_random_build(hero_name)
    return render_template('build.html', build=build)

@app.route('/select-hero')
def select_hero():
    heroes = get_all_heroes()
    return render_template('select_hero.html', heroes=heroes)

@app.route('/select-build')
def select_predefined_build():
    """Страница выбора готового билда"""
    heroes = get_all_heroes()
    return render_template('select_build.html', heroes=heroes)

@app.route('/builds')
def show_builds():
    """Показать готовые билды для героя"""
    hero_name = request.args.get('hero')
    builds = get_predefined_builds(hero_name)
    return render_template('builds_list.html', builds=builds, hero_name=hero_name)

@app.route('/build/<int:build_id>')
def show_predefined_build(build_id):
    """Показать конкретный готовый билд"""
    build = get_predefined_build_by_id(build_id)
    if build:
        return render_template('predefined_build.html', build=build)
    else:
        return "Билд не найден", 404

@app.route('/api/generate')
def api_generate_build():
    hero_name = request.args.get('hero')
    build = generate_random_build(hero_name)
    return jsonify(build)

@app.route('/api/heroes')
def api_get_heroes():
    """API endpoint для получения списка героев"""
    heroes = get_all_heroes()
    return jsonify(heroes)

@app.route('/api/items/<category>')
def api_get_items(category):
    """API endpoint для получения предметов по категории"""
    if not check_db_exists():
        return jsonify([])
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM items WHERE category = ? ORDER BY name', (category,))
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(items)

@app.route('/api/predefined-builds')
def api_get_predefined_builds():
    """API endpoint для получения готовых билдов"""
    hero_name = request.args.get('hero')
    builds = get_predefined_builds(hero_name)
    return jsonify(builds)

if __name__ == '__main__':
    if not check_db_exists():
        print("\nЗАМЕЧАНИЕ: Запустите db_init.py для создания базы данных.")
        print("Приложение будет работать с ограниченной функциональностью.")
    
    # Проверяем наличие placeholder изображения
    if not os.path.exists('static/images/placeholder.jpg'):
        print("\nСоздаю placeholder изображение...")
        from PIL import Image, ImageDraw
        # Создаем простое placeholder изображение
        img = Image.new('RGB', (256, 256), color='#1a1a2e')
        d = ImageDraw.Draw(img)
        d.text((128, 128), "?", fill="#ffffff", anchor="mm")
        os.makedirs('static/images', exist_ok=True)
        img.save('static/images/placeholder.jpg', 'JPEG')
        print("✓ Placeholder изображение создано")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
