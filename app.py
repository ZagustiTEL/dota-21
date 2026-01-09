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

def populate_db():
    """Заполнение базы данных начальными данными"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Герои с изображениями (все герои из обоих файлов)
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
            "Pirate Hat", "Witless Shako", "Magic Lamp", "Giant's Ring", "Spark of Courage",
            "Vindicator's Axe"
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
    
    # Примеры готовых билдов (127 билдов - по одному для каждого героя)
    predefined_builds = [
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
    ]
    
    for build in predefined_builds:
        cursor.execute('''
            INSERT OR IGNORE INTO predefined_builds 
            (hero_name, lane, skill_build, starting_items, early_items, core_items, late_items, neutral_items)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', build)
    
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

def get_predefined_builds(hero_name=None):
    """Получить готовые билды, опционально для конкретного героя"""
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
        hero, hero_image = get_hero_by_name(build['hero'])
        build['hero_image'] = hero_image
        
        builds.append(build)
    
    conn.close()
    return builds

def get_predefined_build_by_id(build_id):
    """Получить готовый билд по ID"""
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
        hero, hero_image = get_hero_by_name(build['hero'])
        build['hero_image'] = hero_image
        
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

@app.route('/api/predefined-builds')
def api_get_predefined_builds():
    """API endpoint для получения готовых билдов"""
    hero_name = request.args.get('hero')
    builds = get_predefined_builds(hero_name)
    return jsonify(builds)

if __name__ == '__main__':
    # Инициализация базы данных при первом запуске
    if not os.path.exists(DB_NAME):
        init_db()
        populate_db()
        print("База данных Doza.db создана и заполнена данными!")
        print(f"Расположение базы данных: {os.path.abspath(DB_NAME)}")
        print("Добавлено 7 готовых билдов для различных героев")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
