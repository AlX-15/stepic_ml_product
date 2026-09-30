from fastapi import FastAPI, UploadFile, File
from PIL import Image
import torch
from torchvision import transforms, models
import json
import io
import uvicorn

# Создаём приложение FastAPI — это наш ML-сервер
app = FastAPI(title="AI-Весы ML-Сервис", version="1.0")

# === 1. ЗАГРУЗКА СПИСКА ПРОДУКТОВ ===
# JSON-файл с русскими названиями: {"0": "Яблоко красное", "1": "Банан", ...}
print("📦 Загружаю список продуктов...")
with open("class_names.json", "r", encoding="utf-8") as f:
    class_names = json.load(f)

num_classes = len(class_names)
print(f"   Загружено {num_classes} категорий продуктов")

# === 2. ЗАГРУЗКА МОДЕЛИ ===
# EfficientNet-B0 — компактная нейросеть для распознавания изображений.
# Мы загружаем архитектуру без предобученных весов (weights=None),
# потому что свои веса мы обучили на Fruits-360 и сохранили в product_model.pth
print("🤖 Загружаю ИИ-модель распознавания продуктов...")

# TODO 1: Создать модель EfficientNet-B0 и заменить последний слой
model = models.efficientnet_b0(weights=None)
model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)

# TODO 2: Загрузить обученные веса из файла product_model.pth (использовать map_location="cpu") и перевести в eval
model.load_state_dict(torch.load("product_model.pth", map_location="cpu"))
model.eval()

# === 3. ПОДГОТОВКА ИЗОБРАЖЕНИЙ ===
# Нейросеть ожидает картинку определённого размера и формата.
# Resize(224, 224) — приводим к размеру, на котором обучалась модель
# ToTensor() — превращаем картинку в числа (тензор)
# Normalize(...) — нормализация по стандартам ImageNet (на них учился EfficientNet)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

print("✅ Модель готова к работе!")

# === 4. РУЧКА /predict ===
# Принимает фото продукта, возвращает top-3 предсказания
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Читаем файл изображения, присланный по сети
    image_bytes = await file.read()
    # Открываем как PIL-картинку и конвертируем в RGB
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Применяем transform и добавляем batch-размерность [1, 3, 224, 224]
    input_tensor = transform(image).unsqueeze(0)

    # TODO 3: Сделать предсказание моделью (без подсчёта градиентов!)
    with torch.no_grad():
        outputs = model(input_tensor)

    # TODO 4: Превратить «сырые» числа модели в вероятности (softmax)
    probabilities = torch.nn.functional.softmax(outputs, dim=0)

    # TODO 5: Взять top-3 самых вероятных класса
    top3_prob, top3_idx = torch.topk(probabilities, 3)

    # TODO 6: Собрать результат в список словарей и вернуть
    results = []
    for i in range(3):
        results.append({
            "name": class_names[top3_idx[i].item()],
            "confidence": round(top3_prob[i].item()*100, 1)
        })
    return {"predictions": results}# Запуск сервера
if __name__ == "__main__":
    print("🚀 ML-сервис запущен на http://localhost:8001")
    print("📖 Документация: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)