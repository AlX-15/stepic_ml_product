// ==========================================
//  AI-ВЕСЫ — Логика интерфейса
// ==========================================

// === ЧАСТЬ А: ЗАГРУЗКА ИЗОБРАЖЕНИЯ ===

// Элементы зоны загрузки (id добавляются в index.html на уроке):
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const previewImg = document.getElementById('preview-img');
const placeholder = document.getElementById('placeholder');

// ═══ 🔶 TODO 1: кнопка btn ═══
// TODO 1: Найди кнопку по id "btn" и сохрани в переменную btn
// const btn = document...

// ═══ 🔶 TODO 2: блок result ═══
// TODO 2: Найди блок результата по id "result" и сохрани в переменную resultBox
// const resultBox = document...

// Переменная для хранения выбранного файла
let selectedFile = null;

// Вспомогательная функция (уже готова): показать превью загруженной картинки
function handleFile(file) {
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        previewImg.style.display = 'block';
        placeholder.style.display = 'none';
        uploadArea.classList.add('has-image');
        btn.disabled = false;
    };
    reader.readAsDataURL(file);
}

// Drag & Drop — перетаскивание файла в зону загрузки (уже готово)
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFile(file);
    }
});

// Клик по зоне — открывает диалог выбора файла (уже готово)
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
});


// === ЧАСТЬ Б: КНОПКА И ЗАПРОС К ИИ ===

btn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // Шаг 1: Показываем загрузку (уже готово)
    resultBox.innerHTML = '<div class="loading">🤖 ИИ анализирует продукт...</div>';
    resultBox.classList.add('active');

    // Шаг 2: Упаковываем файл в FormData
    // ═══ 🔶 TODO 3: FormData ═══
    // TODO 3: Создай объект FormData и добавь в него файл
    // const formData = new ...
    // formData.append('file', selectedFile);

    try {
        // Шаг 3: Отправляем fetch-запрос
        // ═══ 🔶 TODO 4: fetch POST ═══
        // TODO 4: POST на http://localhost:8000/api/recognize (method: 'POST', body: formData)
        // const response = await fetch(...)

        // Шаг 4: Разбираем ответ
        // ═══ 🔶 TODO 5: response.json() ═══
        // TODO 5: Распакуй JSON (.json()) и возьми predictions
        // const data = await response.json();
        // const predictions = data.predictions;

        // Шаг 5: Строим карточки результата
        // ═══ 🔶 TODO 6: карточки результата ═══
        // TODO 6: Цикл predictions.forEach — карточки с медалями и полосой уверенности
        // let html = '';
        // predictions.forEach((pred, index) => { ... });
        // resultBox.innerHTML = html;

    } catch (error) {
        resultBox.innerHTML = '<div class="error">❌ Ошибка! Убедись, что серверы запущены.</div>';
        console.error("Детали ошибки:", error);
    }
});
