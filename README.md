# 🎮 Dota 2 Random Build Generator


## ✨ Возможности

### 🎲 Случайная генерация билдов
- Случайный выбор героя
- Случайная стратегия прокачки навыков
- Предметы для разных стадий игры
- Случайная позиция на карте

### 🎯 Целевые билды
- Выбор конкретного героя
- Готовые проверенные билды
- Просмотр билдов по категориям

### 📊 База данных
- Все герои Dota 2 (более 120)
- Различные категории предметов
- Предопределенные билды

### 🛠 Технологии
- Backend: Flask (Python)
- Database: SQLite
- Frontend: HTML5, CSS3

### 📂Структура проекта

```
Dota2-Build-Generator/
│
├── app.py              # Основное приложение Flask
├── db_init.py          # Инициализация базы данных
├── download_images.py  # Скачивание изображений героев
├── Doza.db             # База данных SQLite (создается автоматически)
│
├── templates/          # HTML шаблоны
│   ├── index.html              # Главная страница
│   ├── select_hero.html        # Выбор героя
│   ├── select_build.html       # Выбор готового билда
│   ├── build.html              # Отображение случайного билда
│   ├── predefined_build.html   # Отображение готового билда
│   └── builds_list.html        # Список готовых билдов
│
└── static/             # Статические файлы
    └── style.css       # Основные стили
```

###Ссылка на сайт
http://192.168.1.17:5000/

### Главное меню сайта
<img width="1703" height="860" alt="image" src="https://github.com/user-attachments/assets/2d6efc63-056b-4db7-a836-f4e0743e5e7c" />

### Меню выбора героев
<img width="1909" height="652" alt="image" src="https://github.com/user-attachments/assets/0c5569b7-c920-405f-b4c4-c4615febc07f" />

### Пример работы сайта
<img width="826" height="891" alt="image" src="https://github.com/user-attachments/assets/a2113e6a-3ec9-422e-a125-c0c5e224738a" />
