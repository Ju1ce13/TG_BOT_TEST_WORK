from dotenv import load_dotenv
import os

load_dotenv()
ECHO_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "sk-neurocoder")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")