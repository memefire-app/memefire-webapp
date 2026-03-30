import httpx
from config import DEFAULT_MEMES

# Бесплатные API для мемов (без ключей)
MEME_APIS = [
    "https://meme-api.com/gimme",  # Reddit memes
    "https://meme-api.com/gimme/wholesomememes",
    "https://meme-api.com/gimme/dankmemes",
    "https://meme-api.com/gimme/memes",
    "https://meme-api.com/gimme/funny",
]


async def fetch_random_memes(count: int = 20) -> list:
    """Получить случайные мемы из интернета"""
    memes = []
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Запрашиваем мемы из разных источников
        for i in range(count):
            try:
                # Выбираем случайный API
                api_url = MEME_APIS[i % len(MEME_APIS)]
                response = await client.get(api_url)
                
                if response.status_code == 200:
                    data = response.json()
                    meme = {
                        "id": str(data.get("id", f"net_{i}")),
                        "imageUrl": data.get("url", DEFAULT_MEMES[i % len(DEFAULT_MEMES)]["imageUrl"]),
                        "title": data.get("title", f"Meme {i}"),
                        "description": data.get("postLink", ""),
                        "tags": [data.get("subreddit", "memes").split("/")[-1]]
                    }
                    memes.append(meme)
            except Exception:
                # Если API не доступен, берём фолбэк
                fallback = DEFAULT_MEMES[i % len(DEFAULT_MEMES)].copy()
                fallback["id"] = f"fallback_{i}"
                memes.append(fallback)
    
    return memes if memes else DEFAULT_MEMES[:count]


async def search_memes_online(query: str, count: int = 20) -> list:
    """Поиск мемов в интернете по запросу"""
    memes = []
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Поиск через Reddit API по сабреддитам
            search_url = f"https://meme-api.com/gimme/{query}"
            response = await client.get(search_url)
            
            if response.status_code == 200:
                data = response.json()
                meme = {
                    "id": str(data.get("id", "search_1")),
                    "imageUrl": data.get("url", DEFAULT_MEMES[0]["imageUrl"]),
                    "title": data.get("title", query),
                    "description": data.get("postLink", ""),
                    "tags": [query]
                }
                memes.append(meme)
        except Exception:
            pass
        
        # Если не нашли, ищем в фолбэках по ключевым словам
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
