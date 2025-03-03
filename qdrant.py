import logging
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter

logger = logging.getLogger(__name__)


class QdrantService:
    def __init__(self, url: str, api_key: str, collection_name: str):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name

    def create_collection(self):
        """
        Создает коллекцию в Qdrant, если она не существует.
        """
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            logger.info(f"Коллекция '{self.collection_name}' создана успешно.")
        except Exception as e:
            logger.warning(f"Коллекция '{self.collection_name}' уже существует или произошла ошибка: {e}")

    def add_message(self, message_id: int, text: str, embedding: list):
        """
        Добавляет сообщение в коллекцию Qdrant.

        :param message_id: ID сообщения.
        :param text: Текст сообщения.
        :param embedding: Эмбеддинг текста.
        """
        point = PointStruct(
            id=message_id,
            vector=embedding,
            payload={"text": text}
        )
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            logger.info(f"Сообщение добавлено в Qdrant: {text}")
        except Exception as e:
            logger.error(f"Ошибка при добавлении сообщения в Qdrant: {e}")

    def find_similar_message(self, embedding: list) -> str | None:
        """
        Ищет похожее сообщение в коллекции Qdrant.

        :param embedding: Эмбеддинг для поиска.
        :return: Текст похожего сообщения или None, если ничего не найдено.
        """
        try:
            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query_filter=Filter(),  # Можно добавить фильтры, если нужно
                query_vector=embedding,
                limit=1,
                with_payload=True,  # Возвращать полезную нагрузку (текст сообщения)
                score_threshold=0.5
            )
            if search_result:
                return search_result[0].payload["text"]
            return None
        except Exception as e:
            logger.error(f"Ошибка при поиске похожего сообщения: {e}")
            return None
