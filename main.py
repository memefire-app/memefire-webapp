from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from config import DEFAULT_MEMES

# Инициализация приложения
app = FastAPI(
    title="Meme API",
    description="API для поиска мемов",
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

# Простой поиск по ключевым словам (без нейросети)
def search_memes(query: str, top_k: int = 20) -> List[dict]:
    """Поиск мемов по ключевым словам"""
    query_lower = query.lower().strip()
    
    if not query_lower:
        return DEFAULT_MEMES[:top_k]
    
    results = []
    for meme in DEFAULT_MEMES:
        score = 0
        # Проверяем совпадения в title
        if query_lower in meme['title'].lower():
            score += 3
        # Проверяем совпадения в description
        if query_lower in meme.get('description', '').lower():
            score += 2
        # Проверяем совпадения в tags
        for tag in meme.get('tags', []):
            if query_lower in tag.lower():
                score += 1
        
        if score > 0:
            meme_copy = meme.copy()
            meme_copy['score'] = score
            results.append(meme_copy)
    
    # Сортируем по релевантности
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results[:top_k]

@app.get("/")
async def root():
    return {
        "message": "Meme API Server",
        "version": "1.0.0",
        "endpoints": {
            "memes": "/api/memes - Получить список мемов",
            "search": "/api/search - Поиск мемов (POST с query)"
        }
    }

@app.get("/api/memes", response_model=MemesResponse)
async def get_memes(limit: int = 20):
    """Получить список мемов"""
    return {"memes": DEFAULT_MEMES[:limit]}

@app.post("/api/search", response_model=SearchResponse)
async def search_memes_endpoint(request: SearchRequest):
    """Поиск мемов по ключевым словам"""
    results = search_memes(request.query, top_k=20)
    
    # Удаляем score из результатов
    for meme in results:
        meme.pop('score', None)
    
    return {"memes": results}

@app.get("/api/health")
async def health_check():
    """Проверка здоровья сервера"""
    return {
        "status": "healthy",
        "memes_count": len(DEFAULT_MEMES)
    }

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
