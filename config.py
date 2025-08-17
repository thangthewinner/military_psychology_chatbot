import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "Alibaba-NLP/gte-multilingual-base")
    
    # Database Configuration
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # LLM Configuration
    LLM_MODEL = "gemini-pro"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # Embedding Configuration
    EMBEDDING_DIMENSION = 768
    BATCH_SIZE = 32
    
    # Vector Search Configuration
    TOP_K_RESULTS = 3
    SIMILARITY_THRESHOLD = 0.7
    
    # Streamlit Configuration
    PAGE_TITLE = "Chatbot Tư vấn Tâm lý Quân nhân"
    PAGE_ICON = "🎖️"
    
    # Data Configuration
    DATA_FILE = "data/military_psychology.csv"
