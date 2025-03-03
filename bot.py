import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from qdrant import QdrantService
from embeddings import EmbeddingService
from config import QDRANT_API_KEY, QDRANT_URL, TELEGRAM_BOT_TOKEN, EMBEDDING_API_URL, EMBEDDING_API_KEY, COLLECTION_NAME

# Проверка наличия обязательных переменных окружения
if not all([QDRANT_URL, QDRANT_API_KEY, TELEGRAM_BOT_TOKEN, EMBEDDING_API_URL, EMBEDDING_API_KEY, COLLECTION_NAME]):
    raise EnvironmentError("Не все переменные окружения заданы. Проверьте файл .env.")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Логирование в файл
        logging.StreamHandler()  # Логирование в консоль
    ]
)
logger = logging.getLogger(__name__)

# Инициализация сервисов
qdrant_service = QdrantService(QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME)
embedding_service = EmbeddingService(EMBEDDING_API_URL, EMBEDDING_API_KEY)

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Отправь мне сообщение, и я найду самое похожее из ранее отправленных.")


# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    user_message = message.text
    message_id = message.message_id

    # Генерация эмбеддинга для текущего сообщения
    embedding = embedding_service.generate_embedding(user_message)
    if embedding is None:
        await message.answer("Ошибка при обработке сообщения.")
        return

    # Поиск похожего сообщения
    similar_message = qdrant_service.find_similar_message(embedding)
    if similar_message:
        await message.answer(f"Похожее сообщение: {similar_message}")
    else:
        await message.answer("Похожих сообщений не найдено.")

    # Добавление текущего сообщения в Qdrant
    qdrant_service.add_message(message_id, user_message, embedding)


# Запуск бота
async def main():
    qdrant_service.create_collection()  # Создание коллекции при запуске
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
