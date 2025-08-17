"""
Cấu hình cho ứng dụng chatbot
"""
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Đường dẫn thư mục gốc của dự án
ROOT_DIR = Path(__file__).parent.parent

# Cấu hình API
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Cấu hình mô hình
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "Alibaba-NLP/gte-multilingual-base")

# Cấu hình vector database
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(ROOT_DIR / "vector_db"))

# Cấu hình dữ liệu
DATA_PATH = str(ROOT_DIR / "data" / "military_psychology.csv")

# Cấu hình logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FOLDER = os.getenv("LOG_FOLDER", str(ROOT_DIR / "logs"))
LOG_FILENAME = f"{datetime.now().strftime('%Y-%m-%d')}.log"
LOG_PATH = str(Path(LOG_FOLDER) / LOG_FILENAME)

# Cấu hình RAG
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3

# Cấu hình Streamlit
STREAMLIT_TITLE = "Chatbot Tư Vấn Tâm Lý Quân Nhân"
STREAMLIT_DESCRIPTION = "Hệ thống hỗ trợ tư vấn tâm lý cho quân nhân dựa trên công nghệ AI"