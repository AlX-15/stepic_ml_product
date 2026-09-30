from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn

app = FastAPI(title="AI-Весы Главный Бэкенд", version="1.0")

# === 1. CORS — «Паспортный контроль» ===
# Браузер по умолчанию блокирует запросы с одного адреса на другой.
# Например, файл index.html (порт 5500) → сервер (порт 8000) будет заблокирован.
# CORSMiddleware говорит: «Мы доверяем всем, пускаем всех» (allow_origins=["*"])
# В боевом проекте вместо "*" указывают конкретный адрес сайта!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 2. ГЛАВНАЯ РУЧКА — МОСТ ===
@app.post("/api/recognize")
async def recognize(file: UploadFile = File(...)):
    """
    Принимает фото от сайта, перенаправляет в ML-сервис, возвращает результат.

    Архитектура:
    Сайт (5500) → Этот сервер (8000) → ML-сервис (8001) → назад
    """
    print(f"📸 Получено фото: {file.filename}")
    print("📞 Отправляю в ML-сервис на порт 8001...")

    # Адрес нашего ML-микросервиса (запущен отдельно!)
    ml_url = "http://localhost:8001/predict"

    # Читаем файл, который прислал браузер
    file_bytes = await file.read()

    # TODO 1: Отправить файл в ML-сервис через requests.post
    # Подсказка: requests.post(url, files={"file": (имя, байты, тип)})
    response = requests.post(ml_url, files={"file": (file.filename, file_bytes, file.content_type)})

    # TODO 2: Распаковать ответ в словарь и вернуть его
    ai_answer = response.json()
    return ai_answer


if __name__ == "__main__":
    print("🚀 Главный бэкенд запущен на http://localhost:8000")
    print("   Убедитесь, что ML-сервис (порт 8001) уже запущен!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
