from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import random
import time
from meme_fetcher import fetch_random_memes, search_memes_online
from config import DEFAULT_MEMES

# Инициализация приложения
app = FastAPI(
    title="Meme API",
    description="API для поиска мемов из интернета",
    version="1.0.0"
)

# Разрешаем CORS для Android приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class Meme(BaseModel):
    id: str
    imageUrl: str
    title: str
    description: Optional[str] = ""
    tags: List[str] = []

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    memes: List[Meme]

class MemesResponse(BaseModel):
    memes: List[Meme]

# Кэш для мемов (чтобы не запрашивать каждый раз)
meme_cache = []
cache_timestamp = 0

@app.get("/")
async def root():
    return {
        "message": "Meme API Server",
        "version": "1.0.0",
        "endpoints": {
            "memes": "/api/memes - Получить случайные мемы из интернета",
            "search": "/api/search - Поиск мемов (POST с query)"
        }
    }

@app.get("/api/memes", response_model=MemesResponse)
async def get_memes(limit: int = 20, force_refresh: bool = False):
    """Получить случайные мемы из интернета"""
    global meme_cache, cache_timestamp
    
    # Кэшируем на 5 минут
    current_time = time.time()
    if not meme_cache or force_refresh or (current_time - cache_timestamp) > 300:
        try:
            meme_cache = await fetch_random_memes(limit)
            cache_timestamp = current_time
        except Exception as e:
            # Возвращаем фолбэк из config.py
            meme_cache = random.sample(DEFAULT_MEMES, min(limit, len(DEFAULT_MEMES)))
    
    # Возвращаем случайную выборку из кэша
    result = random.sample(meme_cache, min(limit, len(meme_cache))) if len(meme_cache) > limit else meme_cache
    return {"memes": result}

@app.post("/api/search", response_model=SearchResponse)
async def search_memes_endpoint(request: SearchRequest):
    """Поиск мемов в интернете по запросу"""
    if not request.query.strip():
        # Пустой запрос - возвращаем случайные из фолбэка
        return {"memes": random.sample(DEFAULT_MEMES, min(20, len(DEFAULT_MEMES)))}
    
    try:
        results = await search_memes_online(request.query, count=20)
        return {"memes": results}
    except Exception as e:
        # Фолбэк - поиск локально в DEFAULT_MEMES
        query_lower = request.query.lower()
        filtered = [
            m for m in DEFAULT_MEMES 
            if query_lower in m["title"].lower() or 
               query_lower in " ".join(m["tags"]).lower() or
               query_lower in m.get("description", "").lower()
        ]
        return {"memes": filtered if filtered else random.sample(DEFAULT_MEMES, 20)}

@app.get("/api/health")
async def health_check():
    """Проверка здоровья сервера"""
    return {
        "status": "healthy",
        "cache_size": len(meme_cache),
        "fallback_count": len(DEFAULT_MEMES)
    }

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
