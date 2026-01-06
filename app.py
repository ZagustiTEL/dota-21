from flask import Flask, render_template, request, jsonify
import random
import sqlite3
import os

app = Flask(__name__)

# Имя базы данных
DB_NAME = 'Doza.db'

def init_db():
    """Инициализация базы данных и создание таблиц"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица героев
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            image_url TEXT
        )
    ''')
    
    # Таблица предметов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT
        )
    ''')
    
    # Таблица стратегий прокачки
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_builds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    # Таблица линий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lanes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def populate_db():
    """Заполнение базы данных начальными данными"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Герои с изображениями
    heroes = [
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
    
    for hero_name, hero_image in heroes:
        cursor.execute('INSERT OR IGNORE INTO heroes (name, image_url) VALUES (?, ?)', 
                      (hero_name, hero_image))
    
    # Предметы
    items_data = {
        "starting": [
            "Tango", "Healing Salve", "Clarity", "Iron Branch", "Gauntlets of Strength", 
            "Slippers of Agility", "Mantle of Intelligence", "Circlet", "Magic Stick",
            "Enchanted Mango", "Faerie Fire"
        ],
        "early": [
            "Magic Wand", "Boots of Speed", "Bracer", "Wraith Band", "Null Talisman",
            "Soul Ring", "Power Treads", "Phase Boots", "Arcane Boots", "Hand of Midas"
        ],
        "core": [
            "Black King Bar", "Blink Dagger", "Force Staff", "Aghanim's Scepter",
            "Shadow Blade", "Desolator", "Maelstrom", "Battle Fury", "Radiance",
            "Armlet of Mordiggian", "Crystalys", "Echo Sabre", "Dragon Lance"
        ],
        "late": [
            "Abyssal Blade", "Butterfly", "Daedalus", "Divine Rapier", "Eye of Skadi",
            "Heart of Tarrasque", "Monkey King Bar", "Mjollnir", "Nullifier",
            "Satanic", "Skull Basher", "Silver Edge", "Bloodthorn", "Assault Cuirass",
            "Shiva's Guard", "Scythe of Vyse", "Linken's Sphere", "Lotus Orb",
            "Refresher Orb", "Aghanim's Blessing", "Octarine Core"
        ],
        "neutral": [
            "Faded Broach", "Ocean Heart", "Iron Talon", "Royal Jelly", "Pupil's Gift",
            "Trusty Shovel", "Quickening Charm", "Philosopher's Stone", "Essence Ring",
            "Grove Bow", "Elven Tunic", "Cloak of Flames", "Titan Sliver", "Mind Breaker",
            "Spell Prism", "Ninja Gear", "Illusionist's Cape", "Timeless Relic",
            "Fusion Rune", "Mirror Shield", "Apex", "Ballista", "Book of the Dead",
            "Ex Machina", "Fallen Sky", "Seer Stone", "Stygian Desolator", "The Leveller",
            "Pirate Hat", "Witless Shako", "Magic Lamp", "Giant's Ring"
        ]
    }
    
    for category, items in items_data.items():
        for item in items:
            cursor.execute('INSERT OR IGNORE INTO items (name, category) VALUES (?, ?)', (item, category))
    
    # Стратегии прокачки
    skill_builds = {
        "aggressive": ["Maximize damage skills first", "Focus on early game dominance"],
        "defensive": ["Maximize survival skills", "Focus on sustain and escape"],
        "farming": ["Maximize farming abilities", "Focus on late game scaling"],
        "utility": ["Maximize crowd control", "Focus on team support"],
        "hybrid": ["Balanced skill build", "Adapt to game situation"]
    }
    
    for build_type, descriptions in skill_builds.items():
        for desc in descriptions:
            cursor.execute('INSERT OR IGNORE INTO skill_builds (type, description) VALUES (?, ?)', (build_type, desc))
    
    # Линии
    lanes = ["Safe Lane", "Mid Lane", "Off Lane", "Soft Support", "Hard Support"]
    for lane in lanes:
        cursor.execute('INSERT OR IGNORE INTO lanes (name) VALUES (?)', (lane,))
    
    conn.commit()
    conn.close()

def get_random_hero():
    """Получить случайного героя из базы данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, image_url FROM heroes ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result[0], result[1]  # Имя и URL изображения

def get_hero_by_name(hero_name):
    """Получить героя по имени"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, image_url FROM heroes WHERE name = ?', (hero_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0], result[1]
    return None, None

def get_all_heroes():
    """Получить всех героев"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM heroes ORDER BY name')
    heroes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return heroes

def get_random_lane():
    """Получить случайную линию из базы данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM lanes ORDER BY RANDOM() LIMIT 1')
    lane = cursor.fetchone()[0]
    conn.close()
    return lane

def get_random_skill_build():
    """Получить случайную стратегию прокачки из базы данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT type, description FROM skill_builds ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result[1]  # Возвращаем описание

def get_random_items(category, limit):
    """Получить случайные предметы определенной категории"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM items WHERE category = ? ORDER BY RANDOM() LIMIT ?', (category, limit))
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items

def generate_random_build(hero_name=None):
    """Генерация случайного билда с использованием данных из базы данных"""
    if hero_name:
        hero, hero_image = get_hero_by_name(hero_name)
        if not hero:
            # Если герой не найден, берем случайного
            hero, hero_image = get_random_hero()
    else:
        hero, hero_image = get_random_hero()
    
    lane = get_random_lane()
    skill_build = get_random_skill_build()
    
    # Генерация предметов
    starting_items = get_random_items("starting", 6)
    early_items = get_random_items("early", 3)
    core_items = get_random_items("core", 3)
    late_items = get_random_items("late", 2)
    neutral_items = get_random_items("neutral", 2)
    
    build = {
        "hero": hero,
        "hero_image": hero_image,
        "lane": lane,
        "skill_build": skill_build,
        "starting_items": starting_items,
        "early_game": early_items,
        "core_items": core_items,
        "late_game": late_items,
        "neutral_items": neutral_items
    }
    
    return build

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

@app.route('/api/generate')
def api_generate_build():
    hero_name = request.args.get('hero')
    build = generate_random_build(hero_name)
    return jsonify(build)

@app.route('/api/heroes')
def api_get_heroes():
    """API endpoint для получения списка героев"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM heroes ORDER BY name')
    heroes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(heroes)

@app.route('/api/items/<category>')
def api_get_items(category):
    """API endpoint для получения предметов по категории"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM items WHERE category = ? ORDER BY name', (category,))
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(items)

if __name__ == '__main__':
    # Инициализация базы данных при первом запуске
    if not os.path.exists(DB_NAME):
        init_db()
        populate_db()
        print("База данных Doza.db создана и заполнена данными!")
        print(f"Расположение базы данных: {os.path.abspath(DB_NAME)}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
