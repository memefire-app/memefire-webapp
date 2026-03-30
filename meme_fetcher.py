import httpx
from config import DEFAULT_MEMES
import random

# Бесплатные API для мемов (без ключей) - с резервными вариантами
MEME_APIS = [
    "https://meme-api.com/gimme",  # Reddit memes
    "https://meme-api.com/gimme/wholesomememes",
    "https://meme-api.com/gimme/dankmemes",
    "https://meme-api.com/gimme/memes",
    "https://meme-api.com/gimme/funny",
    # Резервные API
    "https://www.reddit.com/r/memes/random.json",
    "https://www.reddit.com/r/dankmemes/random.json",
]

# Заголовки для обхода блокировок
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


async def fetch_random_memes(count: int = 20) -> list:
    """Получить случайные мемы из интернета"""
    memes = []

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(10.0, connect=5.0, read=10.0),
        headers=HEADERS,
        follow_redirects=True
    ) as client:
        # Запрашиваем мемы из разных источников
        for i in range(count):
            success = False
            # Пробуем несколько API подряд
            for attempt in range(3):
                try:
                    # Выбираем случайный API
                    api_url = random.choice(MEME_APIS)
                    response = await client.get(api_url)

                    if response.status_code == 200:
                        data = response.json()
                        # Обработка Reddit API
                        if isinstance(data, list) and len(data) > 0:
                            data = data[0].get("data", {}).get("children", [{}])[0].get("data", {})
                        
                        url = data.get("url") or data.get("imageUrl")
                        if url and url.startswith("http"):
                            meme = {
                                "id": str(data.get("id", f"net_{i}_{attempt}")),
                                "imageUrl": url,
                                "title": data.get("title", f"Meme {i}"),
                                "description": data.get("postLink", data.get("permalink", "")),
                                "tags": [data.get("subreddit", "memes").split("/")[-1] if data.get("subreddit") else "memes"]
                            }
                            memes.append(meme)
                            success = True
                            break
                except Exception:
                    # Пробуем следующий API
                    continue
            
            # Если все API не доступны, берём фолбэк
            if not success:
                fallback = DEFAULT_MEMES[i % len(DEFAULT_MEMES)].copy()
                fallback["id"] = f"fallback_{i}"
                memes.append(fallback)

    return memes if memes else DEFAULT_MEMES[:count]


async def search_memes_online(query: str, count: int = 20) -> list:
    """Поиск мемов в интернете по запросу"""
    memes = []

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(10.0, connect=5.0, read=10.0),
        headers=HEADERS,
        follow_redirects=True
    ) as client:
        # Пробуем несколько вариантов поиска
        search_urls = [
            f"https://meme-api.com/gimme/{query}",
            f"https://www.reddit.com/r/{query}/search.json?q={query}&sort=relevance&limit={count}",
        ]
        
        for search_url in search_urls:
            try:
                response = await client.get(search_url)
                if response.status_code == 200:
                    data = response.json()
                    # Обработка Reddit API
                    if isinstance(data, list) and len(data) > 0:
                        children = data[0].get("data", {}).get("children", [])
                    else:
                        children = data.get("data", {}).get("children", [])
                    
                    for child in children[:count]:
                        post_data = child.get("data", {})
                        url = post_data.get("url") or post_data.get("imageUrl")
                        if url and url.startswith("http"):
                            meme = {
                                "id": str(post_data.get("id", f"search_{len(memes)}")),
                                "imageUrl": url,
                                "title": post_data.get("title", query),
                                "description": post_data.get("permalink", ""),
                                "tags": [query, post_data.get("subreddit", "memes")]
                            }
                            memes.append(meme)
                    
                    if memes:
                        break
            except Exception:
                continue

        # Если не нашли в интернете, ищем в фолбэках по ключевым словам
        if not memes:
            query_lower = query.lower()
            for meme in DEFAULT_MEMES:
                if (query_lower in meme["title"].lower() or
                    query_lower in " ".join(meme["tags"]).lower() or
                    query_lower in meme.get("description", "").lower()):
                    memes.append(meme.copy())
                    if len(memes) >= count:
                        break

    return memes if memes else DEFAULT_MEMES[:count]
