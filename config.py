import os
from pathlib import Path

# Создаём директорию для мемов если не существует
MEMES_DIR = Path(__file__).parent / "memes"
MEMES_DIR.mkdir(exist_ok=True)

# Базовые данные мемов (в реальном приложении - база данных)
DEFAULT_MEMES = [
    {
        "id": "1",
        "imageUrl": "https://i.imgflip.com/1g8my4.jpg",
        "title": "Two Buttons",
        "description": "Мем с двумя кнопками для выбора сложного решения",
        "tags": ["выбор", "решение", "кнопки", "сложный выбор"]
    },
    {
        "id": "2",
        "imageUrl": "https://i.imgflip.com/1h7in3.jpg",
        "title": "Change My Mind",
        "description": "Стивен Краудер за столом с табличкой",
        "tags": ["спор", "мнение", "дискуссия", "измени мнение"]
    },
    {
        "id": "3",
        "imageUrl": "https://i.imgflip.com/1ur4b8.jpg",
        "title": "Distracted Boyfriend",
        "description": "Парень смотрит на другую девушку",
        "tags": ["отношения", "выбор", "внимание", "девушка"]
    },
    {
        "id": "4",
        "imageUrl": "https://i.imgflip.com/261o3j.jpg",
        "title": "Drake Hotline Bling",
        "description": "Дрейк отвергает и одобряет варианты",
        "tags": ["предпочтение", "выбор", "драйк", "одобрение"]
    },
    {
        "id": "5",
        "imageUrl": "https://i.imgflip.com/30b1gx.jpg",
        "title": "Woman Yelling at Cat",
        "description": "Женщина кричит на кота за столом",
        "tags": ["спор", "кот", "крик", "конфликт"]
    },
    {
        "id": "6",
        "imageUrl": "https://i.imgflip.com/1bij.jpg",
        "title": "One Does Not Simply",
        "description": "Боромир из Властелина Колец",
        "tags": ["властелин колец", "задача", "невозможно", "боромир"]
    },
    {
        "id": "7",
        "imageUrl": "https://i.imgflip.com/9ehk.jpg",
        "title": "Success Kid",
        "description": "Малыш с кулаком успеха",
        "tags": ["успех", "победа", "достижение", "радость"]
    },
    {
        "id": "8",
        "imageUrl": "https://i.imgflip.com/265k.jpg",
        "title": "Ancient Aliens",
        "description": "Парень с теорией о древних пришельцах",
        "tags": ["конспирология", "пришельцы", "теория", "космос"]
    },
    {
        "id": "9",
        "imageUrl": "https://i.imgflip.com/4t0m5.jpg",
        "title": "Batman Slapping Robin",
        "description": "Бэтмен бьёт Робина",
        "tags": ["реакция", "стоп", "прекрати", "бэтмен"]
    },
    {
        "id": "10",
        "imageUrl": "https://i.imgflip.com/1x6lm.jpg",
        "title": "This Is Fine",
        "description": "Собака в горящей комнате",
        "tags": ["стресс", "отрицание", "проблемы", "всё нормально"]
    },
    {
        "id": "11",
        "imageUrl": "https://i.imgflip.com/2gpkch.jpg",
        "title": "Mocking Spongebob",
        "description": "Губка Боб дразнится",
        "tags": ["насмешка", "сарказм", "троллинг", "губка боб"]
    },
    {
        "id": "12",
        "imageUrl": "https://i.imgflip.com/39t1o.jpg",
        "title": "Stonks",
        "description": "Мем про акции и инвестиции",
        "tags": ["акции", "инвестиции", "финансы", "рост"]
    },
    {
        "id": "13",
        "imageUrl": "https://i.imgflip.com/1wokww.jpg",
        "title": "Hide the Pain Harold",
        "description": "Гарольд скрывает боль",
        "tags": ["боль", "скрыть", "страдание", "улыбка"]
    },
    {
        "id": "14",
        "imageUrl": "https://i.imgflip.com/2h7jqr.jpg",
        "title": "Expanding Brain",
        "description": "Расширяющийся мозг с уровнями понимания",
        "tags": ["мозг", "понимание", "интеллект", "эволюция"]
    },
    {
        "id": "15",
        "imageUrl": "https://i.imgflip.com/48058b.jpg",
        "title": "Always Has Been",
        "description": "Астронавты в космосе",
        "tags": ["космос", "правда", "всегда", "астронавт"]
    }
]
