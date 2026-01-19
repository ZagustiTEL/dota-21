import sqlite3
import os
from pathlib import Path

DB_NAME = 'Doza.db'

def init_db():
    """Инициализация базы данных и создание таблиц"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица героев - теперь храним локальный путь к изображению
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            image_path TEXT
        )
    ''')
    
    # Таблица предметов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL
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
    
    # Таблица готовых билдов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predefined_builds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hero_name TEXT NOT NULL,
            lane TEXT NOT NULL,
            skill_build TEXT NOT NULL,
            starting_items TEXT,
            early_items TEXT,
            core_items TEXT,
            late_items TEXT,
            neutral_items TEXT,
            FOREIGN KEY (hero_name) REFERENCES heroes (name)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Таблицы базы данных созданы успешно!")

def populate_db():
    """Заполнение базы данных начальными данными"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Герои Dota 2 с именами файлов
    heroes = [
        ("Anti-Mage", "anti_mage.jpg"),
        ("Axe", "axe.jpg"),
        ("Bane", "bane.jpg"),
        ("Bloodseeker", "bloodseeker.jpg"),
        ("Crystal Maiden", "crystal_maiden.jpg"),
        ("Drow Ranger", "drow_ranger.jpg"),
        ("Earthshaker", "earthshaker.jpg"),
        ("Juggernaut", "juggernaut.jpg"),
        ("Mirana", "mirana.jpg"),
        ("Morphling", "morphling.jpg"),
        ("Shadow Fiend", "shadow_fiend.jpg"),
        ("Phantom Lancer", "phantom_lancer.jpg"),
        ("Puck", "puck.jpg"),
        ("Pudge", "pudge.jpg"),
        ("Razor", "razor.jpg"),
        ("Sand King", "sand_king.jpg"),
        ("Storm Spirit", "storm_spirit.jpg"),
        ("Sven", "sven.jpg"),
        ("Tiny", "tiny.jpg"),
        ("Vengeful Spirit", "vengeful_spirit.jpg"),
        ("Windranger", "windranger.jpg"),
        ("Zeus", "zeus.jpg"),
        ("Kunkka", "kunkka.jpg"),
        ("Lina", "lina.jpg"),
        ("Lion", "lion.jpg"),
        ("Shadow Shaman", "shadow_shaman.jpg"),
        ("Slardar", "slardar.jpg"),
        ("Tidehunter", "tidehunter.jpg"),
        ("Witch Doctor", "witch_doctor.jpg"),
        ("Riki", "riki.jpg"),
        ("Enigma", "enigma.jpg"),
        ("Tinker", "tinker.jpg"),
        ("Sniper", "sniper.jpg"),
        ("Necrophos", "necrophos.jpg"),
        ("Warlock", "warlock.jpg"),
        ("Beastmaster", "beastmaster.jpg"),
        ("Queen of Pain", "queen_of_pain.jpg"),
        ("Venomancer", "venomancer.jpg"),
        ("Faceless Void", "faceless_void.jpg"),
        ("Wraith King", "wraith_king.jpg"),
        ("Death Prophet", "death_prophet.jpg"),
        ("Phantom Assassin", "phantom_assassin.jpg"),
        ("Pugna", "pugna.jpg"),
        ("Templar Assassin", "templar_assassin.jpg"),
        ("Viper", "viper.jpg"),
        ("Luna", "luna.jpg"),
        ("Dragon Knight", "dragon_knight.jpg"),
        ("Dazzle", "dazzle.jpg"),
        ("Clockwerk", "clockwerk.jpg"),
        ("Leshrac", "leshrac.jpg"),
        ("Nature's Prophet", "natures_prophet.jpg"),
        ("Lifestealer", "lifestealer.jpg"),
        ("Dark Seer", "dark_seer.jpg"),
        ("Clinkz", "clinkz.jpg"),
        ("Omniknight", "omniknight.jpg"),
        ("Enchantress", "enchantress.jpg"),
        ("Huskar", "huskar.jpg"),
        ("Night Stalker", "night_stalker.jpg"),
        ("Broodmother", "broodmother.jpg"),
        ("Bounty Hunter", "bounty_hunter.jpg"),
        ("Weaver", "weaver.jpg"),
        ("Jakiro", "jakiro.jpg"),
        ("Batrider", "batrider.jpg"),
        ("Chen", "chen.jpg"),
        ("Spectre", "spectre.jpg"),
        ("Ancient Apparition", "ancient_apparition.jpg"),
        ("Doom", "doom.jpg"),
        ("Ursa", "ursa.jpg"),
        ("Spirit Breaker", "spirit_breaker.jpg"),
        ("Gyrocopter", "gyrocopter.jpg"),
        ("Alchemist", "alchemist.jpg"),
        ("Invoker", "invoker.jpg"),
        ("Silencer", "silencer.jpg"),
        ("Outworld Destroyer", "outworld_destroyer.jpg"),
        ("Lycan", "lycan.jpg"),
        ("Brewmaster", "brewmaster.jpg"),
        ("Shadow Demon", "shadow_demon.jpg"),
        ("Lone Druid", "lone_druid.jpg"),
        ("Chaos Knight", "chaos_knight.jpg"),
        ("Meepo", "meepo.jpg"),
        ("Treant Protector", "treant_protector.jpg"),
        ("Ogre Magi", "ogre_magi.jpg"),
        ("Undying", "undying.jpg"),
        ("Rubick", "rubick.jpg"),
        ("Disruptor", "disruptor.jpg"),
        ("Nyx Assassin", "nyx_assassin.jpg"),
        ("Naga Siren", "naga_siren.jpg"),
        ("Keeper of the Light", "keeper_of_the_light.jpg"),
        ("Io", "io.jpg"),
        ("Visage", "visage.jpg"),
        ("Slark", "slark.jpg"),
        ("Medusa", "medusa.jpg"),
        ("Troll Warlord", "troll_warlord.jpg"),
        ("Centaur Warrunner", "centaur_warrunner.jpg"),
        ("Magnus", "magnus.jpg"),
        ("Timbersaw", "timbersaw.jpg"),
        ("Bristleback", "bristleback.jpg"),
        ("Tusk", "tusk.jpg"),
        ("Skywrath Mage", "skywrath_mage.jpg"),
        ("Abaddon", "abaddon.jpg"),
        ("Elder Titan", "elder_titan.jpg"),
        ("Legion Commander", "legion_commander.jpg"),
        ("Techies", "techies.jpg"),
        ("Ember Spirit", "ember_spirit.jpg"),
        ("Earth Spirit", "earth_spirit.jpg"),
        ("Underlord", "underlord.jpg"),
        ("Terrorblade", "terrorblade.jpg"),
        ("Phoenix", "phoenix.jpg"),
        ("Oracle", "oracle.jpg"),
        ("Winter Wyvern", "winter_wyvern.jpg"),
        ("Arc Warden", "arc_warden.jpg"),
        ("Monkey King", "monkey_king.jpg"),
        ("Dark Willow", "dark_willow.jpg"),
        ("Pangolier", "pangolier.jpg"),
        ("Grimstroke", "grimstroke.jpg"),
        ("Hoodwink", "hoodwink.jpg"),
        ("Void Spirit", "void_spirit.jpg"),
        ("Snapfire", "snapfire.jpg"),
        ("Mars", "mars.jpg"),
        ("Dawnbreaker", "dawnbreaker.jpg"),
        ("Marci", "marci.jpg"),
        ("Primal Beast", "primal_beast.jpg"),
        ("Muerta", "muerta.jpg")
    ]
    
    # Проверяем наличие папки с изображениями
    image_dir = Path('static/images/heroes')
    if not image_dir.exists():
        print("\nПРЕДУПРЕЖДЕНИЕ: Папка с изображениями не найдена!")
        print("Запустите download_images.py для скачивания изображений.")
        print("Будут использованы placeholder изображения.")
    
    for hero_name, image_file in heroes:
        # Проверяем существует ли файл
        image_path = f"static/images/heroes/{image_file}"
        
        if os.path.exists(image_path):
            cursor.execute('INSERT OR IGNORE INTO heroes (name, image_path) VALUES (?, ?)', 
                          (hero_name, image_path))
        else:
            print(f"Предупреждение: изображение для {hero_name} не найдено ({image_file})")
            # Используем placeholder
            cursor.execute('INSERT OR IGNORE INTO heroes (name, image_path) VALUES (?, ?)', 
                          (hero_name, "static/images/placeholder.jpg"))
    
    print(f"Добавлено {len(heroes)} героев")
    
    # Предметы (остается без изменений)
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
            "Pirate Hat", "Witless Shako", "Magic Lamp", "Giant's Ring", "Spark of Courage",
            "Vindicator's Axe"
        ]
    }
    
    total_items = 0
    for category, items in items_data.items():
        for item in items:
            cursor.execute('INSERT OR IGNORE INTO items (name, category) VALUES (?, ?)', (item, category))
            total_items += 1
    
    print(f"Добавлено {total_items} предметов")
    
    # Стратегии прокачки
    skill_builds = {
        "aggressive": ["Maximize damage skills first", "Focus on early game dominance"],
        "defensive": ["Maximize survival skills", "Focus on sustain and escape"],
        "farming": ["Maximize farming abilities", "Focus on late game scaling"],
        "utility": ["Maximize crowd control", "Focus on team support"],
        "hybrid": ["Balanced skill build", "Adapt to game situation"]
    }
    
    total_skill_builds = 0
    for build_type, descriptions in skill_builds.items():
        for desc in descriptions:
            cursor.execute('INSERT OR IGNORE INTO skill_builds (type, description) VALUES (?, ?)', (build_type, desc))
            total_skill_builds += 1
    
    print(f"Добавлено {total_skill_builds} стратегий прокачки")
    
    # Линии
    lanes = ["Safe Lane", "Mid Lane", "Off Lane", "Soft Support", "Hard Support"]
    for lane in lanes:
        cursor.execute('INSERT OR IGNORE INTO lanes (name) VALUES (?)', (lane,))
    
    print(f"Добавлено {len(lanes)} линий")
    
    # Примеры готовых билдов (127 героев × 3 билда = 381 билд, кроме Abaddon у которого уже 2 билда)
    predefined_builds = [
        # Существующие билды (127 билдов)
        # Билд для Anti-Mage
        ("Anti-Mage", "Safe Lane", "Maximize Blink and Mana Break", 
         "Tango,Quelling Blade,Circlet,Slippers of Agility", 
         "Power Treads,Wraith Band,Magic Wand", 
         "Battle Fury,Manta Style", 
         "Abyssal Blade,Butterfly", 
         "Faded Broach,Philosopher's Stone"),
        
        # Билд для Crystal Maiden
        ("Crystal Maiden", "Hard Support", "Maximize Crystal Nova and Frostbite",
         "Tango,Clarity,Enchanted Mango,Circlet",
         "Tranquil Boots,Magic Wand,Bracer",
         "Glimmer Cape,Force Staff",
         "Aghanim's Scepter,Boots of Travel",
         "Iron Talon,Trusty Shovel"),
        
        # Билд для Pudge
        ("Pudge", "Soft Support", "Maximize Meat Hook and Rot",
         "Tango,Healing Salve,Gauntlets of Strength",
         "Magic Wand,Phase Boots,Bracer",
         "Blink Dagger,Hood of Defiance",
         "Heart of Tarrasque,Aghanim's Scepter",
         "Ocean Heart,Grove Bow"),
        
        # Билд для Juggernaut
        ("Juggernaut", "Safe Lane", "Maximize Blade Fury and Omnislash",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Magic Wand,Phase Boots,Wraith Band",
         "Battle Fury,Manta Style",
         "Skull Basher,Butterfly",
         "Trusty Shovel,Elven Tunic"),
        
        # Билд для Shadow Fiend
        ("Shadow Fiend", "Mid Lane", "Maximize Shadowraze and Necromastery",
         "Tango,Faerie Fire,Branch,Mantle of Intelligence",
         "Bottle,Magic Wand,Power Treads",
         "Eul's Scepter,Black King Bar",
         "Butterfly,Satanic",
         "Philosopher's Stone,Pupil's Gift"),
        
        # Билд для Earthshaker
        ("Earthshaker", "Hard Support", "Maximize Fissure and Echo Slam",
         "Tango,Clarity,Gauntlets of Strength,Circlet",
         "Arcane Boots,Magic Wand,Bracer",
         "Blink Dagger,Force Staff",
         "Aghanim's Scepter,Refresher Orb",
         "Ocean Heart,Iron Talon"),
        
        # Билд для Invoker
        ("Invoker", "Mid Lane", "Maximize Quas, Wex, Exort equally",
         "Tango,Faerie Fire,Branch,Mantle of Intelligence",
         "Bottle,Magic Wand,Power Treads",
         "Aghanim's Scepter,Octarine Core",
         "Refresher Orb,Shiva's Guard",
         "Pupil's Gift,Spell Prism"),

         # Билд для Invoker через радиацию
        ("Invoker", "Mid Lane", "Maximize Quas",
         "Tango,Faerie Fire,Branch,Mantle of Intelligence",
         "Bottle,Magic Wand,Power Treads",
         "Aghanim's shard, Radiance",
         "aghanim's scepter,Yasha and Kaya",
         "Pupil's Gift,Spell Prism"),
        
        # Билд для Axe
        ("Axe", "Off Lane", "Maximize Counter Helix, farm with Battle Hunger",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Vanguard,Phase Boots,Magic Wand",
         "Blade Mail,Blink Dagger",
         "Black King Bar,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Windranger
        ("Windranger", "Mid Lane", "Maximize Powershot and Windrun",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Magic Wand",
         "Maelstrom,Aghanim's Scepter",
         "Monkey King Bar,Daedalus",
         "Spark of Courage,Philosopher's Stone"),
        
        # Билд для Earthshaker (Soft Support)
        ("Earthshaker", "Soft Support", "Maximize Fissure, roam and gank",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Bracer,Magic Wand",
         "Blink Dagger,Aghanim's Shard",
         "Black King Bar,Aghanim's Scepter",
         "Spark of Courage"),
        
        # Билд для Phantom Assassin
        ("Phantom Assassin", "Safe Lane", "Maximize Stifling Dagger and Blur",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Battle Fury,Desolator",
         "Basher,Black King Bar",
         "Faded Broach"),
        
        # Билд для Invoker (Quas-Wex)
        ("Invoker", "Mid Lane", "Quas-Wex for control and damage",
         "Tango,Faerie Fire,Branches,Branches",
         "Hand of Midas,Power Treads,Bracer",
         "Orchid Malevolence,Aghanim's Scepter",
         "Octarine Core,Shiva's Guard",
         "Vindicator's Axe,Spark of Courage"),
        
        # Билд для Lion
        ("Lion", "Hard Support", "Maximize Earth Spike and Hex, secure kills",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Wand,Wind Lace",
         "Blink Dagger,Aghanim's Shard",
         "Aghanim's Scepter,Force Staff",
         "Philosopher's Stone"),
        
        # Билд для Shadow Fiend (альтернативный)
        ("Shadow Fiend", "Mid Lane", "Maximize Necromastery and Raze",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Eul's Scepter,BKB",
         "Butterfly,Skadi",
         "Faded Broach"),
        
        # Билд для Tidehunter
        ("Tidehunter", "Off Lane", "Maximize Anchor Smash, farm and survive",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Bracer",
         "Blink Dagger,Shiva's Guard",
         "Refresher Orb,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Ursa
        ("Ursa", "Safe Lane", "Maximize Fury Swipes, fight early",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Phase Boots,Morbid Mask,Magic Wand",
         "Diffusal Blade,Basher",
         "Abyssal Blade,Skadi",
         "Spark of Courage"),
        
        # Билд для Rubick
        ("Rubick", "Soft Support", "Maximize Telekinesis and Fade Bolt",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Wand,Aether Lens",
         "Blink Dagger,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Templar Assassin
        ("Templar Assassin", "Mid Lane", "Maximize Psi Blades and Refraction",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Desolator,Dragon Lance",
         "Daedalus,Black King Bar",
         "Faded Broach"),
        
        # Билд для Io
        ("Io", "Hard Support", "Maximize Tether and Spirits, save allies",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Soul Ring,Tranquil Boots,Wand",
         "Holy Locket,Mekansm",
         "Guardian Greaves,Heart of Tarrasque",
         "Philosopher's Stone"),
        
        # Билд для Zeus
        ("Zeus", "Mid Lane", "Maximize Arc Lightning and Bolt",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Aether Lens,Aghanim's Scepter",
         "Refresher Orb,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Билд для Slark
        ("Slark", "Safe Lane", "Maximize Essence Shift, pick off heroes",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Diffusal Blade,Echo Sabre",
         "Skadi,Abyssal Blade",
         "Faded Broach"),
        
        # Билд для Dark Willow
        ("Dark Willow", "Soft Support", "Maximize Bramble Maze and Shadow Realm",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Wand,Wind Lace",
         "Eul's Scepter,Aghanim's Shard",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Mars
        ("Mars", "Off Lane", "Maximize Spear and Bulwark, initiate fights",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Phase Boots,Bracer",
         "Blink Dagger,Desolator",
         "Black King Bar,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Grimstroke
        ("Grimstroke", "Hard Support", "Maximize Stroke of Fate and Ink Swell",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Void Spirit
        ("Void Spirit", "Mid Lane", "Maximize Resonant Pulse and Dissimilate",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Eul's Scepter,Kaya and Sange",
         "Shiva's Guard,Octarine Core",
         "Vindicator's Axe,Spark of Courage"),
        
        # Билд для Abaddon
        ("Abaddon", "Soft Support", "Maximize Mist Coil and Aphotic Shield",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Soul Ring",
         "Holy Locket,Pavise",
         "Aghanim's Scepter,Pipe of Insight",
         "Philosopher's Stone,Spark of Courage"),
        
        # Второй билд Abaddon (Off Lane) - добавьте этот
        ("Abaddon", "Off Lane", "Maximize Curse of Avernus and Borrowed Time",
        "Tango,Quelling Blade,Gauntlets of Strength,Branches",
        "Phase Boots,Soul Ring,Bracer",
        "Radiance,Assault Cuirass",
        "Heart of Tarrasque,Shiva's Guard",
        "Vindicator's Axe,Spark of Courage"),

        # Билд для Abaddon (Carry/Safe Lane)
        ("Abaddon", "Safe Lane", "Maximize Curse of Avernus for right-click damage",
        "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
        "Power Treads,Wraith Band,Magic Wand",
        "Radiance,Manta Style",
        "Heart of Tarrasque,Assault Cuirass",
        "Faded Broach,Titan Sliver"),

        # Билд для Alchemist
        ("Alchemist", "Mid Lane", "Maximize Greevil's Greed, farm rapidly",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Hand of Midas,Power Treads,Magic Wand",
         "Radiance,Black King Bar",
         "Assault Cuirass,Overwhelming Blink",
         "Faded Broach,Vindicator's Axe"),
        
        # Билд для Ancient Apparition
        ("Ancient Apparition", "Hard Support", "Maximize Cold Feet and Ice Vortex",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Arc Warden
        ("Arc Warden", "Mid Lane", "Maximize Flux and Spark Wraith",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Magic Wand",
         "Midas,Maelstrom",
         "Mage Slayer,Bloodthorn",
         "Faded Broach,Spark of Courage"),
        
        # Билд для Bane
        ("Bane", "Hard Support", "Maximize Brain Sap and Nightmare",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Batrider
        ("Batrider", "Off Lane", "Maximize Sticky Napalm and Firefly",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Tranquil Boots,Magic Wand",
         "Blink Dagger,Force Staff",
         "Black King Bar,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Beastmaster
        ("Beastmaster", "Off Lane", "Maximize Call of the Wild, push lanes",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Phase Boots,Bracer",
         "Helm of the Overlord,Aghanim's Scepter",
         "Assault Cuirass,Refresher Orb",
         "Spark of Courage"),
        
        # Билд для Bloodseeker
        ("Bloodseeker", "Safe Lane", "Maximize Bloodrage and Thirst",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Basher",
         "Abyssal Blade,Skadi",
         "Faded Broach"),
        
        # Билд для Bounty Hunter
        ("Bounty Hunter", "Soft Support", "Maximize Jinada and Track",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Phase Boots,Orb of Corrosion,Magic Wand",
         "Aghanim's Scepter,Desolator",
         "Nullifier,Bloodthorn",
         "Spark of Courage"),
        
        # Билд для Brewmaster
        ("Brewmaster", "Off Lane", "Maximize Cinder Brew and Drunken Brawler",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Black King Bar,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Bristleback
        ("Bristleback", "Off Lane", "Maximize Quill Spray and Bristleback",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Vanguard,Soul Ring,Phase Boots",
         "Aghanim's Shard,Bloodstone",
         "Octarine Core,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Broodmother
        ("Broodmother", "Off Lane", "Maximize Spawn Spiderlings, split push",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Power Treads,Orb of Corrosion",
         "Diffusal Blade,Black King Bar",
         "Aghanim's Scepter,Skadi",
         "Spark of Courage"),
        
        # Билд для Centaur Warrunner
        ("Centaur Warrunner", "Off Lane", "Maximize Double Edge and Hoof Stomp",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Vanguard,Phase Boots,Soul Ring",
         "Blink Dagger,Hood of Defiance",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Chaos Knight
        ("Chaos Knight", "Safe Lane", "Maximize Chaos Bolt and Reality Rift",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Magic Wand",
         "Echo Sabre,Heart of Tarrasque",
         "Assault Cuirass,Overwhelming Blink",
         "Faded Broach,Spark of Courage"),
        
        # Билд для Chen
        ("Chen", "Hard Support", "Maximize Penitence, control creeps",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Mekansm,Magic Wand",
         "Holy Locket,Vladmir's Offering",
         "Aghanim's Scepter,Guardian Greaves",
         "Philosopher's Stone"),
        
        # Билд для Clinkz
        ("Clinkz", "Safe Lane", "Maximize Searing Arrows and Strafe",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Orchid Malevolence,Dragon Lance",
         "Bloodthorn,Gleipnir",
         "Faded Broach"),
        
        # Билд для Clockwerk
        ("Clockwerk", "Off Lane", "Maximize Battery Assault and Hookshot",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Phase Boots,Bracer",
         "Blade Mail,Force Staff",
         "Black King Bar,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Dark Seer
        ("Dark Seer", "Off Lane", "Maximize Ion Shell and Vacuum",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Bracer",
         "Aghanim's Shard,Pipe of Insight",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage"),
        
        # Билд для Dawnbreaker
        ("Dawnbreaker", "Off Lane", "Maximize Starbreaker and Celestial Hammer",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Aghanim's Shard,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Dazzle
        ("Dazzle", "Hard Support", "Maximize Shadow Wave and Shallow Grave",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Holy Locket,Solar Crest",
         "Aghanim's Scepter,Pavise",
         "Philosopher's Stone"),
        
        # Билд для Death Prophet
        ("Death Prophet", "Mid Lane", "Maximize Crypt Swarm and Spirit Siphon",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Kaya",
         "Eul's Scepter,Aghanim's Shard",
         "Shiva's Guard,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        # Билд для Disruptor
        ("Disruptor", "Hard Support", "Maximize Thunder Strike and Glimpse",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Refresher Orb",
         "Philosopher's Stone"),
        
        # Билд для Doom
        ("Doom", "Off Lane", "Maximize Devour and Scorched Earth",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Shiva's Guard",
         "Refresher Orb,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Dragon Knight
        ("Dragon Knight", "Mid Lane", "Maximize Dragon Tail and Breathe Fire",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Power Treads,Bracer",
         "Blink Dagger,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Drow Ranger
        ("Drow Ranger", "Safe Lane", "Maximize Precision Aura and Multishot",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Wraith Band,Power Treads,Magic Wand",
         "Dragon Lance,Mask of Madness",
         "Butterfly,Daedalus",
         "Faded Broach"),
        
        # Билд для Earth Spirit
        ("Earth Spirit", "Soft Support", "Maximize Boulder Smash and Rolling Boulder",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Soul Ring,Arcane Boots,Magic Wand",
         "Spirit Vessel,Blink Dagger",
         "Black King Bar,Aghanim's Scepter",
         "Spark of Courage"),
        
        # Билд для Elder Titan
        ("Elder Titan", "Off Lane", "Maximize Echo Stomp and Astral Spirit",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Phase Boots,Bracer",
         "Aghanim's Shard,Shiva's Guard",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Ember Spirit
        ("Ember Spirit", "Mid Lane", "Maximize Searing Chains and Sleight of Fist",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Magic Wand",
         "Maelstrom,Aghanim's Scepter",
         "Shiva's Guard,Daedalus",
         "Vindicator's Axe,Faded Broach"),
        
        # Билд для Enchantress
        ("Enchantress", "Off Lane", "Maximize Untouchable and Impetus",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Power Treads,Dragon Lance,Magic Wand",
         "Aghanim's Shard,Pike",
         "Butterfly,Skadi",
         "Spark of Courage"),
        
        # Билд для Enigma
        ("Enigma", "Off Lane", "Maximize Demonic Conversion and Midnight Pulse",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Magic Wand",
         "Blink Dagger,Black King Bar",
         "Refresher Orb,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Faceless Void
        ("Faceless Void", "Safe Lane", "Maximize Time Walk and Time Lock",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Mask of Madness",
         "Manta Style,Butterfly",
         "Aghanim's Scepter,Bloodthorn",
         "Faded Broach"),
        
        # Билд для Gyrocopter
        ("Gyrocopter", "Safe Lane", "Maximize Rocket Barrage and Flak Cannon",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Dragon Lance",
         "Black King Bar,Daedalus",
         "Faded Broach"),
        
        # Билд для Hoodwink
        ("Hoodwink", "Soft Support", "Maximize Acorn Shot and Bushwhack",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Power Treads,Magic Wand,Maelstrom",
         "Gleipnir,Aghanim's Scepter",
         "Bloodthorn,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        # Билд для Huskar
        ("Huskar", "Mid Lane", "Maximize Burning Spear and Berserker's Blood",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Armlet of Mordiggian,Power Treads,Magic Wand",
         "Aghanim's Shard,Satanic",
         "Black King Bar,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Jakiro
        ("Jakiro", "Hard Support", "Maximize Dual Breath and Liquid Fire",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Eul's Scepter",
         "Aghanim's Scepter,Shiva's Guard",
         "Philosopher's Stone"),
        
        # Билд для Keeper of the Light
        ("Keeper of the Light", "Soft Support", "Maximize Illuminate and Blinding Light",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Soul Ring",
         "Aghanim's Shard,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Kunkka
        ("Kunkka", "Mid Lane", "Maximize Tidebringer and X Marks the Spot",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Bottle,Phase Boots,Bracer",
         "Shadow Blade,Daedalus",
         "Silver Edge,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Билд для Legion Commander
        ("Legion Commander", "Off Lane", "Maximize Moment of Courage and Press the Attack",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blade Mail,Blink Dagger",
         "Black King Bar,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Leshrac
        ("Leshrac", "Mid Lane", "Maximize Diabolic Edict and Pulse Nova",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Kaya",
         "Bloodstone,Eul's Scepter",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        # Билд для Lifestealer
        ("Lifestealer", "Safe Lane", "Maximize Feast and Rage",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Armlet of Mordiggian,Phase Boots,Magic Wand",
         "Desolator,Basher",
         "Abyssal Blade,Assault Cuirass",
         "Faded Broach"),
        
        # Билд для Lina
        ("Lina", "Mid Lane", "Maximize Dragon Slave and Fiery Soul",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Magic Wand",
         "Eul's Scepter,Kaya",
         "Aghanim's Scepter,Bloodthorn",
         "Vindicator's Axe,Spark of Courage"),
        
        # Билд для Lone Druid
        ("Lone Druid", "Off Lane", "Maximize Spirit Bear and Savage Roar",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Mask of Madness,Magic Wand",
         "Desolator,Assault Cuirass",
         "Aghanim's Scepter,Overwhelming Blink",
         "Spark of Courage"),
        
        # Билд для Luna
        ("Luna", "Safe Lane", "Maximize Lucent Beam and Moon Glaives",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Dragon Lance",
         "Butterfly,Daedalus",
         "Faded Broach"),
        
        # Билд для Lycan
        ("Lycan", "Off Lane", "Maximize Summon Wolves and Shapeshift",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Helm of the Overlord,Power Treads,Bracer",
         "Assault Cuirass,Black King Bar",
         "Aghanim's Scepter,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Magnus
        ("Magnus", "Off Lane", "Maximize Shockwave and Empower",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Power Treads,Bracer",
         "Blink Dagger,Black King Bar",
         "Refresher Orb,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Marci
        ("Marci", "Soft Support", "Maximize Dispose and Rebound",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Phase Boots,Magic Wand,Soul Ring",
         "Aghanim's Shard,Echo Sabre",
         "Black King Bar,Basher",
         "Spark of Courage"),
        
        # Билд для Medusa
        ("Medusa", "Safe Lane", "Maximize Split Shot and Mystic Snake",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Dragon Lance",
         "Skadi,Butterfly",
         "Faded Broach"),
        
        # Билд для Meepo
        ("Meepo", "Mid Lane", "Maximize Earthbind and Poof",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Power Treads,Blink Dagger,Wraith Band",
         "Dragon Lance,Ethereal Blade",
         "Eye of Skadi,Divine Rapier",
         "Faded Broach"),
        
        # Билд для Mirana
        ("Mirana", "Soft Support", "Maximize Sacred Arrow and Starstorm",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Power Treads,Magic Wand,Maelstrom",
         "Gleipnir,Aghanim's Scepter",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        # Билд для Monkey King
        ("Monkey King", "Off Lane", "Maximize Jingu Mastery and Boundless Strike",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Orb of Corrosion,Magic Wand",
         "Basher,Echo Sabre",
         "Abyssal Blade,Black King Bar",
         "Spark of Courage"),
        
        # Билд для Morphling
        ("Morphling", "Safe Lane", "Maximize Adaptive Strike and Waveform",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Dragon Lance,Ethereal Blade",
         "Skadi,Butterfly",
         "Faded Broach"),
        
        # Билд для Muerta
        ("Muerta", "Safe Lane", "Maximize Dead Shot and The Calling",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Dragon Lance",
         "Aghanim's Scepter,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        # Билд для Naga Siren
        ("Naga Siren", "Safe Lane", "Maximize Mirror Image and Ensnare",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Diffusal Blade",
         "Butterfly,Heart of Tarrasque",
         "Faded Broach"),
        
        # Билд для Nature's Prophet
        ("Nature's Prophet", "Off Lane", "Maximize Teleportation and Sprout",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Hand of Midas,Power Treads,Magic Wand",
         "Gleipnir,Orchid Malevolence",
         "Bloodthorn,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Necrophos
        ("Necrophos", "Mid Lane", "Maximize Death Pulse and Heartstopper Aura",
         "Tango,Faerie Fire,Branches,Branches",
         "Power Treads,Wraith Band,Magic Wand",
         "Radiance,Aghanim's Shard",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Билд для Night Stalker
        ("Night Stalker", "Off Lane", "Maximize Void and Hunter in the Night",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Bracer,Soul Ring",
         "Aghanim's Shard,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Nyx Assassin
        ("Nyx Assassin", "Soft Support", "Maximize Impale and Spiked Carapace",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Dagon",
         "Aghanim's Scepter,Ethereal Blade",
         "Spark of Courage"),
        
        # Билд для Ogre Magi
        ("Ogre Magi", "Hard Support", "Maximize Ignite and Fireblast",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wand",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Shiva's Guard",
         "Philosopher's Stone"),
        
        # Билд для Omniknight
        ("Omniknight", "Off Lane", "Maximize Purification and Heavenly Grace",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Phase Boots,Bracer",
         "Holy Locket,Pipe of Insight",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Oracle
        ("Oracle", "Hard Support", "Maximize Fortune's End and Purifying Flames",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Outworld Destroyer
        ("Outworld Destroyer", "Mid Lane", "Maximize Astral Imprisonment and Sanity's Eclipse",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Magic Wand",
         "Witch Blade,Kaya and Sange",
         "Aghanim's Scepter,Shiva's Guard",
         "Vindicator's Axe,Spark of Courage"),
        
        # Билд для Pangolier
        ("Pangolier", "Off Lane", "Maximize Swashbuckle and Shield Crash",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Diffusal Blade,Phase Boots,Soul Ring",
         "Maelstrom,Aghanim's Scepter",
         "Butterfly,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Phantom Lancer
        ("Phantom Lancer", "Safe Lane", "Maximize Spirit Lance and Doppelganger",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Diffusal Blade,Manta Style",
         "Heart of Tarrasque,Butterfly",
         "Faded Broach"),
        
        # Билд для Phoenix
        ("Phoenix", "Soft Support", "Maximize Icarus Dive and Fire Spirits",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Soul Ring",
         "Shiva's Guard,Aghanim's Shard",
         "Radiance,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Primal Beast
        ("Primal Beast", "Off Lane", "Maximize Onslaught and Trample",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Black King Bar",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Puck
        ("Puck", "Mid Lane", "Maximize Illusory Orb and Waning Rift",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Magic Wand",
         "Witch Blade,Eul's Scepter",
         "Dagon 5,Octarine Core",
         "Vindicator's Axe,Spark of Courage"),
        
        # Билд для Pugna
        ("Pugna", "Mid Lane", "Maximize Nether Blast and Life Drain",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Magic Wand",
         "Aether Lens,Aghanim's Shard",
         "Dagon,Scythe of Vyse",
         "Spark of Courage,Vindicator's Axe"),
        
        # Билд для Queen of Pain
        ("Queen of Pain", "Mid Lane", "Maximize Shadow Strike and Scream of Pain",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Magic Wand",
         "Witch Blade,Aghanim's Scepter",
         "Shiva's Guard,Bloodthorn",
         "Vindicator's Axe,Spark of Courage"),
        
        # Билд для Razor
        ("Razor", "Mid Lane", "Maximize Plasma Field and Static Link",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Power Treads,Falcon Blade,Magic Wand",
         "Aghanim's Shard,Black King Bar",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage"),
        
        # Билд для Riki
        ("Riki", "Safe Lane", "Maximize Tricks of the Trade and Cloak and Dagger",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Diffusal Blade",
         "Manta Style,Basher",
         "Abyssal Blade,Butterfly",
         "Faded Broach"),
        
        # Билд для Sand King
        ("Sand King", "Off Lane", "Maximize Burrowstrike and Sand Storm",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Bracer",
         "Blink Dagger,Veil of Discord",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Shadow Demon
        ("Shadow Demon", "Hard Support", "Maximize Shadow Poison and Demonic Purge",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Shadow Shaman
        ("Shadow Shaman", "Hard Support", "Maximize Ether Shock and Shackles",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Blink Dagger",
         "Aghanim's Scepter,Refresher Orb",
         "Philosopher's Stone"),
        
        # Билд для Silencer
        ("Silencer", "Soft Support", "Maximize Glaives of Wisdom and Last Word",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Power Treads,Wraith Band,Magic Wand",
         "Witch Blade,Aghanim's Scepter",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage"),
        
        # Билд для Skywrath Mage
        ("Skywrath Mage", "Hard Support", "Maximize Arcane Bolt and Concussive Shot",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Rod of Atos",
         "Aether Lens,Aghanim's Scepter",
         "Octarine Core,Bloodthorn",
         "Philosopher's Stone"),
        
        # Билд для Slardar
        ("Slardar", "Off Lane", "Maximize Slithereen Crush and Bash of the Deep",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Power Treads,Blink Dagger,Bracer",
         "Aghanim's Shard,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Snapfire
        ("Snapfire", "Soft Support", "Maximize Scatterblast and Lil' Shredder",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Force Staff,Aghanim's Shard",
         "Aghanim's Scepter,Octarine Core",
         "Spark of Courage"),
        
        # Билд для Sniper
        ("Sniper", "Mid Lane", "Maximize Take Aim and Shrapnel",
         "Tango,Faerie Fire,Branches,Branches",
         "Power Treads,Wraith Band,Magic Wand",
         "Mask of Madness,Dragon Lance",
         "Maelstrom,Daedalus",
         "Faded Broach"),
        
        # Билд для Spectre
        ("Spectre", "Safe Lane", "Maximize Desolate and Dispersion",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Blade Mail,Manta Style",
         "Skadi,Abyssal Blade",
         "Faded Broach"),
        
        # Билд для Spirit Breaker
        ("Spirit Breaker", "Soft Support", "Maximize Charge of Darkness and Greater Bash",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Phase Boots,Magic Wand,Wind Lace",
         "Aghanim's Shard,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Storm Spirit
        ("Storm Spirit", "Mid Lane", "Maximize Electric Vortex and Ball Lightning",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Kaya",
         "Orchid Malevolence,Bloodstone",
         "Aghanim's Scepter,Shiva's Guard",
         "Vindicator's Axe,Spark of Courage"),
        
        # Билд для Sven
        ("Sven", "Safe Lane", "Maximize Great Cleave and God's Strength",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Echo Sabre,Magic Wand",
         "Blink Dagger,Black King Bar",
         "Daedalus,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Билд для Techies
        ("Techies", "Soft Support", "Maximize Sticky Bomb and Reactive Taser",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Soul Ring",
         "Aether Lens,Aghanim's Shard",
         "Octarine Core,Bloodthorn",
         "Spark of Courage"),
        
        # Билд для Terrorblade
        ("Terrorblade", "Safe Lane", "Maximize Metamorphosis and Reflection",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Skadi",
         "Butterfly,Bloodthorn",
         "Faded Broach"),
        
        # Билд для Timbersaw
        ("Timbersaw", "Off Lane", "Maximize Whirling Death and Reactive Armor",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Bracer",
         "Kaya and Sange,Aghanim's Shard",
         "Shiva's Guard,Bloodstone",
         "Spark of Courage"),
        
        # Билд для Tinker
        ("Tinker", "Mid Lane", "Maximize Laser and Heat-Seeking Missile",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Soul Ring,Magic Wand",
         "Aether Lens,Shiva's Guard",
         "Dagon 5,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Билд для Tiny
        ("Tiny", "Mid Lane", "Maximize Avalanche and Toss",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Power Treads,Echo Sabre,Magic Wand",
         "Blink Dagger,Black King Bar",
         "Daedalus,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Билд для Treant Protector
        ("Treant Protector", "Hard Support", "Maximize Leech Seed and Living Armor",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aghanim's Shard,Shiva's Guard",
         "Aghanim's Scepter,Overwhelming Blink",
         "Spark of Courage"),
        
        # Билд для Troll Warlord
        ("Troll Warlord", "Safe Lane", "Maximize Berserker's Rage and Fervor",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Mask of Madness,Sange and Yasha",
         "Silver Edge,Daedalus",
         "Faded Broach"),
        
        # Билд для Tusk
        ("Tusk", "Soft Support", "Maximize Ice Shards and Snowball",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Phase Boots,Magic Wand,Soul Ring",
         "Blink Dagger,Aghanim's Shard",
         "Desolator,Assault Cuirass",
         "Spark of Courage"),
        
        # Билд для Underlord
        ("Underlord", "Off Lane", "Maximize Firestorm and Pit of Malice",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Bracer",
         "Pipe of Insight,Crimson Guard",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Undying
        ("Undying", "Off Lane", "Maximize Decay and Tombstone",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Bracer",
         "Aghanim's Shard,Pipe of Insight",
         "Heart of Tarrasque,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Vengeful Spirit
        ("Vengeful Spirit", "Hard Support", "Maximize Magic Missile and Wave of Terror",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Power Treads,Magic Wand,Wind Lace",
         "Aghanim's Shard,Solar Crest",
         "Aghanim's Scepter,Butterfly",
         "Spark of Courage"),
        
        # Билд для Venomancer
        ("Venomancer", "Soft Support", "Maximize Poison Sting and Plague Ward",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aghanim's Shard,Veil of Discord",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage"),
        
        # Билд для Viper
        ("Viper", "Mid Lane", "Maximize Poison Attack and Nethertoxin",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Power Treads,Wraith Band,Magic Wand",
         "Aghanim's Shard,Dragon Lance",
         "Black King Bar,Skadi",
         "Spark of Courage"),
        
        # Билд для Visage
        ("Visage", "Mid Lane", "Maximize Soul Assumption and Gravekeeper's Cloak",
         "Tango,Faerie Fire,Branches,Branches",
         "Power Treads,Wraith Band,Magic Wand",
         "Solar Crest,Aghanim's Shard",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage"),
        
        # Билд для Warlock
        ("Warlock", "Hard Support", "Maximize Fatal Bonds and Chaotic Offering",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aghanim's Shard,Refresher Orb",
         "Aghanim's Scepter,Shiva's Guard",
         "Philosopher's Stone"),
        
        # Билд для Weaver
        ("Weaver", "Safe Lane", "Maximize The Swarm and Germinate",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Wraith Band,Power Treads,Magic Wand",
         "Maelstrom,Dragon Lance",
         "Daedalus,Butterfly",
         "Faded Broach"),
        
        # Билд для Winter Wyvern
        ("Winter Wyvern", "Hard Support", "Maximize Splinter Blast and Cold Embrace",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Glimmer Cape,Aghanim's Shard",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Witch Doctor
        ("Witch Doctor", "Hard Support", "Maximize Paralyzing Cask and Maledict",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aghanim's Shard,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone"),
        
        # Билд для Wraith King
        ("Wraith King", "Safe Lane", "Maximize Wraithfire Blast and Mortal Strike",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Magic Wand",
         "Radiance,Blink Dagger",
         "Assault Cuirass,Heart of Tarrasque",
         "Faded Broach,Spark of Courage"),

        # ДОПОЛНИТЕЛЬНЫЕ БИЛДЫ (по 2 на каждого героя, кроме Abaddon у которого уже 2)
        
        # Anti-Mage дополнительные билды
        ("Anti-Mage", "Mid Lane", "Maximize Mana Void early, aggressive playstyle",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Manta Style,Basher",
         "Abyssal Blade,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Anti-Mage", "Safe Lane", "Farming build, maximize Battle Fury timing",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Battle Fury,Manta Style,Skadi",
         "Abyssal Blade,Butterfly,Heart of Tarrasque",
         "Philosopher's Stone,Faded Broach"),
        
        # Axe дополнительные билды
        ("Axe", "Off Lane", "Tank build, maximize survivability",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Vanguard,Phase Boots,Bracer",
         "Blade Mail,Blink Dagger,Hood of Defiance",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        ("Axe", "Soft Support", "Roaming build, early ganks",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Blink Dagger,Bracer",
         "Force Staff,Aghanim's Shard",
         "Aghanim's Scepter,Shiva's Guard",
         "Ocean Heart,Spark of Courage"),
        
        # Bane дополнительные билды
        ("Bane", "Soft Support", "Aggressive support, maximize Fiend's Grip",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Essence Ring"),
        
        ("Bane", "Off Lane", "Core Bane, maximize Enfeeble",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Bloodseeker дополнительные билды
        ("Bloodseeker", "Mid Lane", "Maximize Blood Rite, magical damage",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Eul's Scepter,Kaya and Sange",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Bloodseeker", "Off Lane", "Tanky initiator build",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Vanguard,Phase Boots,Soul Ring",
         "Blademail,Black King Bar",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Crystal Maiden дополнительные билды
        ("Crystal Maiden", "Soft Support", "Maximize Frostbite, aggressive support",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Essence Ring"),
        
        ("Crystal Maiden", "Mid Lane", "Core CM, maximize Crystal Nova",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Kaya and Sange,Aghanim's Scepter",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Drow Ranger дополнительные билды
        ("Drow Ranger", "Mid Lane", "Maximize Gust, defensive build",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Dragon Lance,Manta Style",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        ("Drow Ranger", "Safe Lane", "Aghanim's build, maximize Multishot",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Dragon Lance,Aghanim's Scepter",
         "Butterfly,Daedalus",
         "Faded Broach,Titan Sliver"),
        
        # Earthshaker дополнительные билды
        ("Earthshaker", "Off Lane", "Core Earthshaker, maximize Aftershock",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Refresher Orb,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Earthshaker", "Mid Lane", "Mid Earthshaker, max Fissure",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Blink Dagger,Eul's Scepter",
         "Aghanim's Scepter,Octarine Core",
         "Spark of Courage,Pupil's Gift"),
        
        # Juggernaut дополнительные билды
        ("Juggernaut", "Mid Lane", "Maximize Healing Ward, sustain build",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Wraith Band",
         "Manta Style,Skadi",
         "Abyssal Blade,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Juggernaut", "Safe Lane", "Aghanim's build, Swift Slash focus",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Aghanim's Scepter,Manta Style",
         "Abyssal Blade,Butterfly",
         "Faded Broach,Titan Sliver"),
        
        # Mirana дополнительные билды
        ("Mirana", "Mid Lane", "Maximize Sacred Arrow, skillshot focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Maelstrom,Aghanim's Scepter",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Mirana", "Safe Lane", "Carry Mirana, maximize Leap",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Butterfly",
         "Daedalus,Skadi",
         "Faded Broach,Titan Sliver"),
        
        # Morphling дополнительные билды
        ("Morphling", "Mid Lane", "Maximize Adaptive Strike, shotgun build",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Ethereal Blade,Dagon",
         "Aghanim's Scepter,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Morphling", "Safe Lane", "Tanky Morphling, strength morph",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Eye of Skadi,Satanic",
         "Butterfly,Heart of Tarrasque",
         "Faded Broach,Titan Sliver"),
        
        # Shadow Fiend дополнительные билды
        ("Shadow Fiend", "Safe Lane", "Carry SF, max Presence of the Dark Lord",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Shadow Blade,Desolator",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        ("Shadow Fiend", "Mid Lane", "Magical SF, max Razes",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Eul's Scepter,Kaya and Sange",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        # Phantom Lancer дополнительные билды
        ("Phantom Lancer", "Mid Lane", "Maximize Spirit Lance, aggressive build",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Diffusal Blade,Manta Style",
         "Heart of Tarrasque,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Phantom Lancer", "Safe Lane", "Illusion spam build",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Diffusal Blade,Manta Style,Aghanim's Scepter",
         "Heart of Tarrasque,Butterfly,Skadi",
         "Faded Broach,Illusionist's Cape"),
        
        # Puck дополнительные билды
        ("Puck", "Safe Lane", "Carry Puck, right-click build",
         "Tango,Faerie Fire,Branches,Branches",
         "Power Treads,Witch Blade,Wraith Band",
         "Desolator,Aghanim's Scepter",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Puck", "Off Lane", "Offlane Puck, utility build",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Eul's Scepter,Blink Dagger",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        # Pudge дополнительные билды
        ("Pudge", "Mid Lane", "Mid Pudge, max Meat Hook",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Heart of Tarrasque,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Pudge", "Off Lane", "Tank Pudge, max Flesh Heap",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Vanguard,Phase Boots,Soul Ring",
         "Blade Mail,Hood of Defiance",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Razor дополнительные билды
        ("Razor", "Safe Lane", "Carry Razor, max Plasma Field",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Aghanim's Scepter,Black King Bar",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        ("Razor", "Off Lane", "Utility Razor, max Static Link",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Aghanim's Shard,Blade Mail",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Sand King дополнительные билды
        ("Sand King", "Mid Lane", "Mid Sand King, max Burrowstrike",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Sand King", "Safe Lane", "Carry Sand King, right-click build",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Black King Bar",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        # Storm Spirit дополнительные билды
        ("Storm Spirit", "Safe Lane", "Carry Storm, farm build",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Orchid Malevolence,Bloodstone",
         "Aghanim's Scepter,Shiva's Guard",
         "Faded Broach,Spark of Courage"),
        
        ("Storm Spirit", "Mid Lane", "Ganking Storm, early aggression",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Kaya",
         "Orchid Malevolence,Bloodstone",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        # Sven дополнительные билды
        ("Sven", "Mid Lane", "Mid Sven, max Storm Hammer",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Blink Dagger,Black King Bar",
         "Daedalus,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Sven", "Safe Lane", "Farming Sven, max Great Cleave",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Echo Sabre,Magic Wand",
         "Daedalus,Black King Bar",
         "Assault Cuirass,Satanic",
         "Faded Broach,Titan Sliver"),
        
        # Tiny дополнительные билды
        ("Tiny", "Safe Lane", "Carry Tiny, right-click build",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Echo Sabre,Magic Wand",
         "Daedalus,Black King Bar",
         "Assault Cuirass,Silver Edge",
         "Faded Broach,Spark of Courage"),
        
        ("Tiny", "Off Lane", "Utility Tiny, initiator",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Arcane Boots,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        # Vengeful Spirit дополнительные билды
        ("Vengeful Spirit", "Soft Support", "Aura Venge, teamfight build",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Power Treads,Magic Wand,Wind Lace",
         "Solar Crest,Vladmir's Offering",
         "Assault Cuirass,Butterfly",
         "Spark of Courage,Titan Sliver"),
        
        ("Vengeful Spirit", "Safe Lane", "Carry Venge, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Dragon Lance,Manta Style",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        # Windranger дополнительные билды
        ("Windranger", "Safe Lane", "Carry WR, focus fire build",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Aghanim's Scepter",
         "Daedalus,Bloodthorn",
         "Faded Broach,Spark of Courage"),
        
        ("Windranger", "Off Lane", "Utility WR, windrun focus",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Force Staff",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        # Zeus дополнительные билды
        ("Zeus", "Soft Support", "Support Zeus, utility build",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Soul Ring",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Essence Ring"),
        
        ("Zeus", "Safe Lane", "Carry Zeus, right-click build",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Witch Blade,Aghanim's Scepter",
         "Daedalus,Bloodthorn",
         "Faded Broach,Spark of Courage"),
        
        # Kunkka дополнительные билды
        ("Kunkka", "Safe Lane", "Carry Kunkka, cleave build",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Bracer,Magic Wand",
         "Daedalus,Shadow Blade",
         "Silver Edge,Bloodthorn",
         "Faded Broach,Spark of Courage"),
        
        ("Kunkka", "Off Lane", "Utility Kunkka, initiator",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Lina дополнительные билды
        ("Lina", "Safe Lane", "Carry Lina, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Aghanim's Scepter",
         "Daedalus,Bloodthorn",
         "Faded Broach,Spark of Courage"),
        
        ("Lina", "Soft Support", "Support Lina, stun focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Eul's Scepter",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Essence Ring"),
        
        # Lion дополнительные билды
        ("Lion", "Soft Support", "Aggressive Lion, ganking",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Blink Dagger,Aether Lens",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Lion", "Mid Lane", "Core Lion, finger of death focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Shadow Shaman дополнительные билды
        ("Shadow Shaman", "Soft Support", "Aggressive SS, ganking",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Blink Dagger,Aether Lens",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Shadow Shaman", "Mid Lane", "Core SS, pushing focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage,Vindicator's Axe"),
        
        # Slardar дополнительные билды
        ("Slardar", "Safe Lane", "Carry Slardar, bash focus",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Black King Bar",
         "Abyssal Blade,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        ("Slardar", "Mid Lane", "Mid Slardar, ganking",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Black King Bar,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Tidehunter дополнительные билды
        ("Tidehunter", "Mid Lane", "Mid Tide, anchor smash build",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Tidehunter", "Safe Lane", "Carry Tide, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Black King Bar",
         "Daedalus,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Witch Doctor дополнительные билды
        ("Witch Doctor", "Soft Support", "Aggressive WD, maledict focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Witch Doctor", "Mid Lane", "Core WD, death ward focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Riki дополнительные билды
        ("Riki", "Mid Lane", "Mid Riki, smoke screen focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Diffusal Blade,Aghanim's Scepter",
         "Basher,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Riki", "Soft Support", "Support Riki, utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Diffusal Blade,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Enigma дополнительные билды
        ("Enigma", "Mid Lane", "Mid Enigma, midnight pulse focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Blink Dagger,Black King Bar",
         "Refresher Orb,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Enigma", "Safe Lane", "Carry Enigma, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Butterfly",
         "Daedalus,Skadi",
         "Faded Broach,Spark of Courage"),
        
        # Tinker дополнительные билды
        ("Tinker", "Safe Lane", "Carry Tinker, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Dagon,Aghanim's Scepter",
         "Bloodthorn,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Tinker", "Off Lane", "Utility Tinker, defense matrix",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Arcane Boots,Bracer",
         "Aghanim's Shard,Shiva's Guard",
         "Octarine Core,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Sniper дополнительные билды
        ("Sniper", "Safe Lane", "Carry Sniper, headshot focus",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Mask of Madness,Maelstrom",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Sniper", "Off Lane", "Utility Sniper, shrapnel focus",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Aghanim's Shard,Dragon Lance",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Necrophos дополнительные билды
        ("Necrophos", "Safe Lane", "Carry Necro, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Radiance,Heart of Tarrasque",
         "Butterfly,Skadi",
         "Faded Broach,Spark of Courage"),
        
        ("Necrophos", "Off Lane", "Utility Necro, heartstopper aura",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Aghanim's Shard,Pipe of Insight",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Warlock дополнительные билды
        ("Warlock", "Soft Support", "Aggressive Warlock, upheaval focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Warlock", "Mid Lane", "Core Warlock, fatal bonds focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage,Vindicator's Axe"),
        
        # Beastmaster дополнительные билды
        ("Beastmaster", "Safe Lane", "Carry Beastmaster, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Black King Bar",
         "Daedalus,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        ("Beastmaster", "Mid Lane", "Mid Beastmaster, boar focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Helm of the Overlord",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Queen of Pain дополнительные билды
        ("Queen of Pain", "Safe Lane", "Carry QoP, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Orchid Malevolence,Aghanim's Scepter",
         "Bloodthorn,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Queen of Pain", "Soft Support", "Support QoP, scream focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Essence Ring"),
        
        # Venomancer дополнительные билды
        ("Venomancer", "Mid Lane", "Core Veno, poison sting focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Venomancer", "Hard Support", "Support Veno, plague ward focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Faceless Void дополнительные билды
        ("Faceless Void", "Mid Lane", "Mid Void, time walk focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Maelstrom,Aghanim's Scepter",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        ("Faceless Void", "Off Lane", "Offlane Void, chronosphere utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Wraith King дополнительные билды
        ("Wraith King", "Mid Lane", "Mid WK, stun focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Armlet of Mordiggian,Blink Dagger",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Wraith King", "Off Lane", "Utility WK, aura build",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Vladmir's Offering,Assault Cuirass",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Titan Sliver"),
        
        # Death Prophet дополнительные билды
        ("Death Prophet", "Safe Lane", "Carry DP, exorcism focus",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Faded Broach,Spark of Courage"),
        
        ("Death Prophet", "Off Lane", "Utility DP, spirit siphon",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Eul's Scepter,Aghanim's Shard",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Phantom Assassin дополнительные билды
        ("Phantom Assassin", "Mid Lane", "Mid PA, dagger focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Wraith Band",
         "Desolator,Battle Fury",
         "Basher,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Phantom Assassin", "Off Lane", "Offlane PA, blur utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Desolator,Black King Bar",
         "Abyssal Blade,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Pugna дополнительные билды
        ("Pugna", "Safe Lane", "Carry Pugna, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Dagon,Aghanim's Scepter",
         "Bloodthorn,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Pugna", "Soft Support", "Support Pugna, decrepify focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Essence Ring"),
        
        # Templar Assassin дополнительные билды
        ("Templar Assassin", "Safe Lane", "Carry TA, psi blades focus",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Desolator,Dragon Lance",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Templar Assassin", "Off Lane", "Utility TA, meld initiation",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Viper дополнительные билды
        ("Viper", "Safe Lane", "Carry Viper, poison attack focus",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Dragon Lance,Skadi",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        ("Viper", "Off Lane", "Utility Viper, nethertoxin area control",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Aghanim's Shard,Pipe of Insight",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Luna дополнительные билды
        ("Luna", "Mid Lane", "Mid Luna, lucent beam focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Manta Style,Aghanim's Scepter",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        ("Luna", "Off Lane", "Utility Luna, eclipse setup",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Dragon Knight дополнительные билды
        ("Dragon Knight", "Safe Lane", "Carry DK, dragon form focus",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Assault Cuirass,Heart of Tarrasque",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Dragon Knight", "Off Lane", "Utility DK, stun initiation",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Phase Boots,Bracer",
         "Blink Dagger,Black King Bar",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Dazzle дополнительные билды
        ("Dazzle", "Soft Support", "Aggressive Dazzle, poison touch",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Solar Crest",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Dazzle", "Mid Lane", "Core Dazzle, shadow wave focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Clockwerk дополнительные билды
        ("Clockwerk", "Mid Lane", "Mid Clock, rocket flare focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Bracer",
         "Blade Mail,Force Staff",
         "Black King Bar,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Clockwerk", "Soft Support", "Support Clock, cogs utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Force Staff,Aghanim's Shard",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Leshrac дополнительные билды
        ("Leshrac", "Safe Lane", "Carry Lesh, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Bloodstone,Aghanim's Scepter",
         "Shiva's Guard,Octarine Core",
         "Faded Broach,Spark of Courage"),
        
        ("Leshrac", "Off Lane", "Utility Lesh, split earth control",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Eul's Scepter,Blink Dagger",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Nature's Prophet дополнительные билды
        ("Nature's Prophet", "Safe Lane", "Carry NP, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Orchid Malevolence",
         "Bloodthorn,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Nature's Prophet", "Mid Lane", "Mid NP, sprout ganking",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Orchid Malevolence,Blink Dagger",
         "Bloodthorn,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Lifestealer дополнительные билды
        ("Lifestealer", "Mid Lane", "Mid LS, rage focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Bracer",
         "Armlet of Mordiggian,Desolator",
         "Abyssal Blade,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Lifestealer", "Off Lane", "Utility LS, open wounds utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Armlet of Mordiggian,Blink Dagger",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage,Titan Sliver"),
        
        # Dark Seer дополнительные билды
        ("Dark Seer", "Mid Lane", "Mid DS, vacuum wall combo",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Dark Seer", "Safe Lane", "Carry DS, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Butterfly",
         "Daedalus,Skadi",
         "Faded Broach,Spark of Courage"),
        
        # Clinkz дополнительные билды
        ("Clinkz", "Mid Lane", "Mid Clinkz, searing arrows focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Orchid Malevolence,Dragon Lance",
         "Bloodthorn,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Clinkz", "Soft Support", "Support Clinkz, skeleton walk utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Orchid Malevolence,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Omniknight дополнительные билды
        ("Omniknight", "Soft Support", "Support Omni, purification focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Holy Locket,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Omniknight", "Mid Lane", "Core Omni, heavenly grace focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Enchantress дополнительные билды
        ("Enchantress", "Mid Lane", "Mid Ench, impetus focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Dragon Lance,Aghanim's Scepter",
         "Butterfly,Skadi",
         "Faded Broach,Spark of Courage"),
        
        ("Enchantress", "Hard Support", "Support Ench, enchant creep control",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Holy Locket,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Huskar дополнительные билды
        ("Huskar", "Safe Lane", "Carry Huskar, life break focus",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Armlet of Mordiggian,Power Treads,Wraith Band",
         "Satanic,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Faded Broach,Spark of Courage"),
        
        ("Huskar", "Off Lane", "Utility Huskar, berserker's blood tank",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Armlet of Mordiggian,Phase Boots,Soul Ring",
         "Aghanim's Shard,Pipe of Insight",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Night Stalker дополнительные билды
        ("Night Stalker", "Mid Lane", "Mid NS, void focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Bracer",
         "Aghanim's Scepter,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Night Stalker", "Safe Lane", "Carry NS, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Basher,Abyssal Blade",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        # Broodmother дополнительные билды
        ("Broodmother", "Mid Lane", "Mid Brood, web control",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Orchid Malevolence,Diffusal Blade",
         "Bloodthorn,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Broodmother", "Safe Lane", "Carry Brood, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Diffusal Blade,Manta Style",
         "Butterfly,Skadi",
         "Faded Broach,Illusionist's Cape"),
        
        # Bounty Hunter дополнительные билды
        ("Bounty Hunter", "Mid Lane", "Mid BH, jinada focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Wraith Band",
         "Desolator,Aghanim's Scepter",
         "Bloodthorn,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Bounty Hunter", "Hard Support", "Support BH, track utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Solar Crest,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Weaver дополнительные билды
        ("Weaver", "Mid Lane", "Mid Weaver, germinate focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Maelstrom,Dragon Lance",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Weaver", "Soft Support", "Support Weaver, shukuchi utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Medallion of Courage,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Jakiro дополнительные билды
        ("Jakiro", "Soft Support", "Aggressive Jakiro, ice path focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Eul's Scepter,Aether Lens",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Jakiro", "Mid Lane", "Core Jakiro, dual breath focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Kaya and Sange,Aghanim's Scepter",
         "Shiva's Guard,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        # Batrider дополнительные билды
        ("Batrider", "Mid Lane", "Mid Bat, firefly focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Soul Ring",
         "Blink Dagger,Force Staff",
         "Black King Bar,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Batrider", "Safe Lane", "Carry Bat, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Butterfly",
         "Daedalus,Skadi",
         "Faded Broach,Spark of Courage"),
        
        # Chen дополнительные билды
        ("Chen", "Soft Support", "Aggressive Chen, penitence focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Holy Locket,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Chen", "Mid Lane", "Core Chen, hand of god focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Spectre дополнительные билды
        ("Spectre", "Mid Lane", "Mid Spectre, dagger focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Manta Style,Skadi",
         "Abyssal Blade,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Spectre", "Off Lane", "Utility Spectre, dispersion tank",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Vanguard,Phase Boots,Soul Ring",
         "Blade Mail,Radiance",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Ancient Apparition дополнительные билды
        ("Ancient Apparition", "Soft Support", "Aggressive AA, cold feet focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Eul's Scepter",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Ancient Apparition", "Mid Lane", "Core AA, ice blast focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Kaya and Sange,Aghanim's Scepter",
         "Shiva's Guard,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        # Doom дополнительные билды
        ("Doom", "Mid Lane", "Mid Doom, devour focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Doom", "Safe Lane", "Carry Doom, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Radiance,Abyssal Blade",
         "Butterfly,Heart of Tarrasque",
         "Faded Broach,Spark of Courage"),
        
        # Ursa дополнительные билды
        ("Ursa", "Mid Lane", "Mid Ursa, earthshock focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Bracer",
         "Diffusal Blade,Basher",
         "Abyssal Blade,Skadi",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Ursa", "Off Lane", "Utility Ursa, overpower utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage,Titan Sliver"),
        
        # Spirit Breaker дополнительные билды
        ("Spirit Breaker", "Mid Lane", "Mid SB, charge focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Bracer",
         "Shadow Blade,Aghanim's Scepter",
         "Black King Bar,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Spirit Breaker", "Off Lane", "Utility SB, bulldoze tank",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blade Mail,Black King Bar",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Gyrocopter дополнительные билды
        ("Gyrocopter", "Mid Lane", "Mid Gyro, rocket barrage focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Maelstrom,Aghanim's Scepter",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Gyrocopter", "Off Lane", "Utility Gyro, flak cannon utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Aghanim's Shard,Dragon Lance",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Alchemist дополнительные билды
        ("Alchemist", "Safe Lane", "Carry Alch, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Radiance,Abyssal Blade",
         "Butterfly,Heart of Tarrasque",
         "Faded Broach,Spark of Courage"),
        
        ("Alchemist", "Off Lane", "Utility Alch, acid spray utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Phase Boots,Bracer",
         "Radiance,Assault Cuirass",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Titan Sliver"),
        
        # Invoker дополнительные билды
        ("Invoker", "Safe Lane", "Carry Invoker, right-click exort",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Aghanim's Scepter",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Invoker", "Off Lane", "Utility Invoker, quas-wex control",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Orchid Malevolence,Blink Dagger",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        # Silencer дополнительные билды
        ("Silencer", "Mid Lane", "Mid Silencer, last word focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Witch Blade,Aghanim's Scepter",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Silencer", "Hard Support", "Support Silencer, arcane curse",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Outworld Destroyer дополнительные билды
        ("Outworld Destroyer", "Safe Lane", "Carry OD, arcane orb focus",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Witch Blade,Aghanim's Scepter",
         "Butterfly,Skadi",
         "Faded Broach,Spark of Courage"),
        
        ("Outworld Destroyer", "Off Lane", "Utility OD, astral utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Aghanim's Shard,Blink Dagger",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Lycan дополнительные билды
        ("Lycan", "Mid Lane", "Mid Lycan, wolves focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Helm of the Overlord,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Lycan", "Safe Lane", "Carry Lycan, shapeshift focus",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Basher",
         "Abyssal Blade,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Brewmaster дополнительные билды
        ("Brewmaster", "Mid Lane", "Mid Brew, cinder brew focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Blink Dagger,Aghanim's Scepter",
         "Black King Bar,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Brewmaster", "Safe Lane", "Carry Brew, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Basher,Abyssal Blade",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        # Shadow Demon дополнительные билды
        ("Shadow Demon", "Soft Support", "Aggressive SD, disruption focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Shadow Demon", "Mid Lane", "Core SD, shadow poison focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Lone Druid дополнительные билды
        ("Lone Druid", "Mid Lane", "Mid LD, bear focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Wraith Band",
         "Desolator,Assault Cuirass",
         "Aghanim's Scepter,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Lone Druid", "Safe Lane", "Carry LD, hero right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Manta Style,Butterfly",
         "Daedalus,Skadi",
         "Faded Broach,Spark of Courage"),
        
        # Chaos Knight дополнительные билды
        ("Chaos Knight", "Mid Lane", "Mid CK, reality rift focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Armlet of Mordiggian,Echo Sabre",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Chaos Knight", "Off Lane", "Utility CK, chaos bolt initiation",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Meepo дополнительные билды
        ("Meepo", "Safe Lane", "Carry Meepo, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Ethereal Blade,Skadi",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        ("Meepo", "Off Lane", "Utility Meepo, earthbind control",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Power Treads,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Treant Protector дополнительные билды
        ("Treant Protector", "Soft Support", "Aggressive Treant, leech seed",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aghanim's Shard,Blink Dagger",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Treant Protector", "Off Lane", "Core Treant, nature's guise initiation",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Aghanim's Scepter",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Ogre Magi дополнительные билды
        ("Ogre Magi", "Soft Support", "Aggressive Ogre, ignite focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Ogre Magi", "Mid Lane", "Core Ogre, multicast focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Undying дополнительные билды
        ("Undying", "Soft Support", "Aggressive Undying, tombstone focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aghanim's Shard,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Undying", "Mid Lane", "Core Undying, decay focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Rubick дополнительные билды
        ("Rubick", "Mid Lane", "Core Rubick, spell steal focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Rubick", "Hard Support", "Support Rubick, fade bolt utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Essence Ring"),
        
        # Disruptor дополнительные билды
        ("Disruptor", "Soft Support", "Aggressive Disruptor, glimpse focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Disruptor", "Mid Lane", "Core Disruptor, kinetic field focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Refresher Orb",
         "Spark of Courage,Vindicator's Axe"),
        
        # Nyx Assassin дополнительные билды
        ("Nyx Assassin", "Mid Lane", "Core Nyx, vendetta focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Dagon,Aghanim's Scepter",
         "Ethereal Blade,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Nyx Assassin", "Hard Support", "Support Nyx, spiked carapace utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Naga Siren дополнительные билды
        ("Naga Siren", "Mid Lane", "Mid Naga, song setup",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Diffusal Blade,Manta Style",
         "Heart of Tarrasque,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Naga Siren", "Off Lane", "Utility Naga, net utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Soul Ring,Phase Boots,Bracer",
         "Diffusal Blade,Blink Dagger",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Keeper of the Light дополнительные билды
        ("Keeper of the Light", "Mid Lane", "Core KotL, illuminate focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Keeper of the Light", "Hard Support", "Support KotL, blinding light utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Essence Ring"),
        
        # Io дополнительные билды
        ("Io", "Soft Support", "Aggressive Io, spirits focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Holy Locket,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Io", "Mid Lane", "Core Io, tether focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Visage дополнительные билды
        ("Visage", "Safe Lane", "Carry Visage, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Solar Crest,Aghanim's Scepter",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        ("Visage", "Off Lane", "Utility Visage, familiars control",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Solar Crest,Assault Cuirass",
         "Heart of Tarrasque,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        # Slark дополнительные билды
        ("Slark", "Mid Lane", "Mid Slark, pounce focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Diffusal Blade,Echo Sabre",
         "Skadi,Abyssal Blade",
         "Faded Broach,Spark of Courage"),
        
        ("Slark", "Off Lane", "Utility Slark, dark pact utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Diffusal Blade,Blink Dagger",
         "Skadi,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Medusa дополнительные билды
        ("Medusa", "Mid Lane", "Mid Medusa, mystic snake focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Manta Style,Dragon Lance",
         "Skadi,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Medusa", "Off Lane", "Utility Medusa, stone gaze utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Manta Style,Blink Dagger",
         "Skadi,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Troll Warlord дополнительные билды
        ("Troll Warlord", "Mid Lane", "Mid Troll, fervor focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Mask of Madness,Sange and Yasha",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Troll Warlord", "Off Lane", "Utility Troll, whirling axes utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Sange and Yasha,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Centaur Warrunner дополнительные билды
        ("Centaur Warrunner", "Mid Lane", "Mid Centaur, double edge focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Blink Dagger,Hood of Defiance",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Centaur Warrunner", "Safe Lane", "Carry Centaur, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Basher",
         "Abyssal Blade,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Magnus дополнительные билды
        ("Magnus", "Mid Lane", "Mid Magnus, shockwave focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Soul Ring",
         "Blink Dagger,Black King Bar",
         "Refresher Orb,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Magnus", "Safe Lane", "Carry Magnus, empower right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Echo Sabre,Wraith Band",
         "Daedalus,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Faded Broach,Spark of Courage"),
        
        # Timbersaw дополнительные билды
        ("Timbersaw", "Mid Lane", "Mid Timber, whirling death focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Kaya and Sange,Aghanim's Scepter",
         "Shiva's Guard,Bloodstone",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Timbersaw", "Safe Lane", "Carry Timber, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Butterfly",
         "Daedalus,Skadi",
         "Faded Broach,Spark of Courage"),
        
        # Bristleback дополнительные билды
        ("Bristleback", "Mid Lane", "Mid BB, quill spray focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Vanguard,Bloodstone",
         "Octarine Core,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Bristleback", "Safe Lane", "Carry BB, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Basher,Abyssal Blade",
         "Heart of Tarrasque,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Tusk дополнительные билды
        ("Tusk", "Mid Lane", "Mid Tusk, ice shards focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Blink Dagger,Aghanim's Scepter",
         "Desolator,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Tusk", "Off Lane", "Utility Tusk, snowball initiation",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Blink Dagger,Black King Bar",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Titan Sliver"),
        
        # Skywrath Mage дополнительные билды
        ("Skywrath Mage", "Soft Support", "Aggressive Sky, arcane bolt spam",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Rod of Atos,Aether Lens",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Skywrath Mage", "Mid Lane", "Core Sky, mystic flare focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Rod of Atos,Aghanim's Scepter",
         "Octarine Core,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Abaddon - уже имеет 2 билда
        
        # Elder Titan дополнительные билды
        ("Elder Titan", "Mid Lane", "Mid ET, echo stomp focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Aghanim's Scepter,Shiva's Guard",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Elder Titan", "Safe Lane", "Carry ET, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Basher",
         "Abyssal Blade,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Legion Commander дополнительные билды
        ("Legion Commander", "Mid Lane", "Mid LC, overwhelming odds focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Blade Mail,Blink Dagger",
         "Black King Bar,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Legion Commander", "Safe Lane", "Carry LC, right-click duel",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Blink Dagger",
         "Abyssal Blade,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Techies дополнительные билды
        ("Techies", "Mid Lane", "Core Techies, blast off focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Aghanim's Scepter,Octarine Core",
         "Bloodthorn,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Techies", "Hard Support", "Support Techies, mine utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Ember Spirit дополнительные билды
        ("Ember Spirit", "Safe Lane", "Carry Ember, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Battle Fury,Daedalus",
         "Butterfly,Abyssal Blade",
         "Faded Broach,Spark of Courage"),
        
        ("Ember Spirit", "Off Lane", "Utility Ember, sleight utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Maelstrom,Blink Dagger",
         "Shiva's Guard,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        # Earth Spirit дополнительные билды
        ("Earth Spirit", "Mid Lane", "Core Earth, geomagnetic grip focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Spirit Vessel,Aghanim's Scepter",
         "Shiva's Guard,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Earth Spirit", "Hard Support", "Support Earth, rolling boulder utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Spirit Vessel,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Underlord дополнительные билды
        ("Underlord", "Mid Lane", "Mid Underlord, firestorm focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Arcane Boots,Soul Ring",
         "Pipe of Insight,Crimson Guard",
         "Aghanim's Scepter,Shiva's Guard",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Underlord", "Safe Lane", "Carry Underlord, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Radiance,Heart of Tarrasque",
         "Butterfly,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Terrorblade дополнительные билды
        ("Terrorblade", "Mid Lane", "Mid TB, reflection focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Manta Style,Skadi",
         "Butterfly,Bloodthorn",
         "Faded Broach,Spark of Courage"),
        
        ("Terrorblade", "Off Lane", "Utility TB, sunder utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Manta Style,Blink Dagger",
         "Skadi,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Phoenix дополнительные билды
        ("Phoenix", "Mid Lane", "Core Phoenix, sun ray focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Soul Ring",
         "Shiva's Guard,Aghanim's Scepter",
         "Heart of Tarrasque,Octarine Core",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Phoenix", "Hard Support", "Support Phoenix, dive utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Urn of Shadows,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Oracle дополнительные билды
        ("Oracle", "Soft Support", "Aggressive Oracle, fortunes end focus",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Eul's Scepter",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Oracle", "Mid Lane", "Core Oracle, purifying flames focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Winter Wyvern дополнительные билды
        ("Winter Wyvern", "Soft Support", "Aggressive WW, splinter blast",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Tranquil Boots,Magic Wand,Wind Lace",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        ("Winter Wyvern", "Mid Lane", "Core WW, arctic burn focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        # Arc Warden дополнительные билды
        ("Arc Warden", "Safe Lane", "Carry Arc, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Butterfly",
         "Daedalus,Skadi",
         "Faded Broach,Spark of Courage"),
        
        ("Arc Warden", "Off Lane", "Utility Arc, flux utility",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Maelstrom,Blink Dagger",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Monkey King дополнительные билды
        ("Monkey King", "Mid Lane", "Mid MK, boundless strike focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Bracer",
         "Echo Sabre,Basher",
         "Abyssal Blade,Black King Bar",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Monkey King", "Safe Lane", "Carry MK, jingu mastery focus",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Orb of Corrosion,Wraith Band",
         "Basher,Abyssal Blade",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        # Dark Willow дополнительные билды
        ("Dark Willow", "Mid Lane", "Core Willow, cursed crown focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Eul's Scepter,Aghanim's Scepter",
         "Octarine Core,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Dark Willow", "Hard Support", "Support Willow, bedlam utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Glimmer Cape,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Pangolier дополнительные билды
        ("Pangolier", "Mid Lane", "Mid Pango, swashbuckle focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Diffusal Blade,Maelstrom",
         "Butterfly,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Pangolier", "Safe Lane", "Carry Pango, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Diffusal Blade,Manta Style",
         "Butterfly,Daedalus",
         "Faded Broach,Spark of Courage"),
        
        # Grimstroke дополнительные билды
        ("Grimstroke", "Mid Lane", "Core Grim, stroke of fate focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Kaya and Sange,Aghanim's Scepter",
         "Octarine Core,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Grimstroke", "Soft Support", "Aggressive Grim, ink swell",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Aether Lens,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Hoodwink дополнительные билды
        ("Hoodwink", "Mid Lane", "Core Hood, acorn shot focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Maelstrom,Aghanim's Scepter",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Hoodwink", "Hard Support", "Support Hood, bushwhack utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Gleipnir,Force Staff",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Void Spirit дополнительные билды
        ("Void Spirit", "Safe Lane", "Carry Void, right-click",
         "Tango,Quelling Blade,Slippers of Agility,Circlet",
         "Power Treads,Wraith Band,Magic Wand",
         "Maelstrom,Butterfly",
         "Daedalus,Skadi",
         "Faded Broach,Spark of Courage"),
        
        ("Void Spirit", "Off Lane", "Utility Void, dissimilate control",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Eul's Scepter,Blink Dagger",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Snapfire дополнительные билды
        ("Snapfire", "Mid Lane", "Core Snap, scatterblast focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Bracer",
         "Aghanim's Scepter,Octarine Core",
         "Shiva's Guard,Bloodthorn",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Snapfire", "Hard Support", "Support Snap, cookie utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Force Staff,Glimmer Cape",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Mars дополнительные билды
        ("Mars", "Mid Lane", "Mid Mars, spear focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Blink Dagger,Desolator",
         "Black King Bar,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Mars", "Safe Lane", "Carry Mars, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Basher",
         "Abyssal Blade,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Dawnbreaker дополнительные билды
        ("Dawnbreaker", "Mid Lane", "Mid Dawn, starbreaker focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Aghanim's Scepter,Black King Bar",
         "Assault Cuirass,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Dawnbreaker", "Safe Lane", "Carry Dawn, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Desolator,Basher",
         "Abyssal Blade,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Marci дополнительные билды
        ("Marci", "Mid Lane", "Mid Marci, rebound focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Echo Sabre,Aghanim's Scepter",
         "Black King Bar,Basher",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Marci", "Hard Support", "Support Marci, dispose utility",
         "Tango,Gauntlets of Strength,Circlet,Branches",
         "Arcane Boots,Magic Wand,Wind Lace",
         "Force Staff,Solar Crest",
         "Aghanim's Scepter,Octarine Core",
         "Philosopher's Stone,Spark of Courage"),
        
        # Primal Beast дополнительные билды
        ("Primal Beast", "Mid Lane", "Mid PB, onslaught focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Phase Boots,Soul Ring",
         "Blink Dagger,Black King Bar",
         "Heart of Tarrasque,Assault Cuirass",
         "Spark of Courage,Vindicator's Axe"),
        
        ("Primal Beast", "Safe Lane", "Carry PB, right-click",
         "Tango,Quelling Blade,Gauntlets of Strength,Circlet",
         "Power Treads,Armlet of Mordiggian,Wraith Band",
         "Basher,Abyssal Blade",
         "Heart of Tarrasque,Assault Cuirass",
         "Faded Broach,Spark of Courage"),
        
        # Muerta дополнительные билды
        ("Muerta", "Mid Lane", "Mid Muerta, dead shot focus",
         "Tango,Faerie Fire,Branches,Branches",
         "Bottle,Power Treads,Wraith Band",
         "Maelstrom,Aghanim's Scepter",
         "Daedalus,Butterfly",
         "Faded Broach,Spark of Courage"),
        
        ("Muerta", "Off Lane", "Utility Muerta, calling control",
         "Tango,Quelling Blade,Gauntlets of Strength,Branches",
         "Phase Boots,Soul Ring,Bracer",
         "Maelstrom,Blink Dagger",
         "Shiva's Guard,Heart of Tarrasque",
         "Spark of Courage,Vindicator's Axe"),
        
        # Еще один дополнительный билд для некоторых героев, чтобы убедиться, что у всех есть 3 билда
        # Для героев, у которых только 1 билд в основном списке, добавляем 2 дополнительных
    ]
    
    for build in predefined_builds:
        cursor.execute('''
            INSERT OR IGNORE INTO predefined_builds 
            (hero_name, lane, skill_build, starting_items, early_items, core_items, late_items, neutral_items)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', build)
    
    conn.commit()
    conn.close()
    
    total_builds = len(predefined_builds)
    print(f"Добавлено {total_builds} готовых билдов")
    print(f"\nБаза данных успешно заполнена!")

if __name__ == '__main__':
    if os.path.exists(DB_NAME):
        print(f"База данных {DB_NAME} уже существует.")
        answer = input("Пересоздать базу данных? (yes/no): ")
        if answer.lower() == 'yes':
            os.remove(DB_NAME)
            print("Старая база данных удалена.")
        else:
            print("Отмена. Используется существующая база данных.")
            exit()
    
    print("Создание базы данных...")
    init_db()
    populate_db()
    print(f"\nБаза данных {DB_NAME} успешно создана и заполнена!")
    print(f"Расположение: {os.path.abspath(DB_NAME)}")
