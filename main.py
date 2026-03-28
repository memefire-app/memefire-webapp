from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from config import DEFAULT_MEMES

# Инициализация приложения
app = FastAPI(
    title="Meme API",
    description="API для поиска мемов с использованием нейросети",
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

# Класс для семантического поиска
class MemeSearchEngine:
    def __init__(self):
        # Загружаем предобученную модель для эмбеддингов
        # Используем легковесную модель для экономии ресурсов
        print("Загрузка модели для семантического поиска...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("Модель загружена!")
        
        # Подготовка данных мемов
        self.memes = DEFAULT_MEMES
        
        # Создаём текстовые представления для каждого мема
        # (объединяем title, description и tags)
        self.meme_texts = []
        for meme in self.memes:
            text_parts = [
                meme['title'],
                meme.get('description', ''),
                ' '.join(meme.get('tags', []))
            ]
            self.meme_texts.append(' '.join(filter(None, text_parts)))
        
        # Вычисляем эмбеддинги для всех мемов
        print("Вычисление эмбеддингов для мемов...")
        self.meme_embeddings = self.model.encode(self.meme_texts)
        print(f"Готово! Обработано {len(self.memes)} мемов")
    
    def search(self, query: str, top_k: int = 20) -> List[dict]:
        """Поиск релевантных мемов по запросу"""
        # Кодируем запрос
        query_embedding = self.model.encode([query])
        
        # Вычисляем косинусное сходство
        similarities = cosine_similarity(query_embedding, self.meme_embeddings)[0]
        
        # Сортируем по релевантности
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Возвращаем топ мемов
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Только релевантные результаты
                meme = self.memes[idx].copy()
                meme['score'] = float(similarities[idx])
                results.append(meme)
        
        return results
    
    def get_all_memes(self, limit: int = 20) -> List[dict]:
        """Получить все мемы (или лимит)"""
        return self.memes[:limit]

# Инициализация поискового движка
search_engine = None

@app.on_event("startup")
async def startup_event():
    global search_engine
    search_engine = MemeSearchEngine()

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
    memes = search_engine.get_all_memes(limit=limit)
    return {"memes": memes}

@app.post("/api/search", response_model=SearchResponse)
async def search_memes(request: SearchRequest):
    """Поиск мемов с использованием нейросети"""
    if not request.query.strip():
        return {"memes": search_engine.get_all_memes()}
    
    results = search_engine.search(request.query, top_k=20)
    
    # Удаляем score из результатов (не нужен клиенту)
    for meme in results:
        meme.pop('score', None)
    
    return {"memes": results}

@app.get("/api/health")
async def health_check():
    """Проверка здоровья сервера"""
    return {
        "status": "healthy",
        "model_loaded": search_engine is not None,
        "memes_count": len(DEFAULT_MEMES) if search_engine else 0
    }

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
