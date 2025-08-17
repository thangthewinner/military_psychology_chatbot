import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np
import logging
from config import Config

logger = logging.getLogger(__name__)

class EmbeddingSystem:
    """Hệ thống embedding và vector database"""
    
    def __init__(self, model_name: str = None, persist_directory: str = None):
        self.model_name = model_name or Config.EMBEDDING_MODEL
        self.persist_directory = persist_directory or Config.CHROMA_PERSIST_DIRECTORY
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {self.model_name}")
        self.embedding_model = SentenceTransformer(self.model_name)
        
        # Initialize ChromaDB
        logger.info(f"Initializing ChromaDB at: {self.persist_directory}")
        self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Create or get collection
        self.collection_name = "military_psychology_qa"
        try:
            self.collection = self.chroma_client.get_collection(name=self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Military psychology Q&A database"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Tạo embeddings cho danh sách text"""
        try:
            embeddings = self.embedding_model.encode(
                texts, 
                batch_size=Config.BATCH_SIZE,
                show_progress_bar=True
            )
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None, ids: List[str] = None):
        """Thêm documents vào vector database"""
        try:
            # Generate embeddings
            embeddings = self.get_embeddings(documents)
            
            # Generate IDs if not provided
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(documents))]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadata or [{}] * len(documents),
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to collection")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def search_similar(self, query: str, n_results: int = None) -> Dict[str, Any]:
        """Tìm kiếm documents tương tự"""
        try:
            # Generate query embedding
            query_embedding = self.get_embeddings([query])[0]
            
            # Search in collection
            n_results = n_results or Config.TOP_K_RESULTS
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise
    
    def search_by_text(self, query: str, n_results: int = None) -> Dict[str, Any]:
        """Tìm kiếm bằng text (ChromaDB sẽ tự động tạo embedding)"""
        try:
            n_results = n_results or Config.TOP_K_RESULTS
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching by text: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Lấy thông tin collection"""
        try:
            count = self.collection.count()
            return {
                "name": self.collection_name,
                "document_count": count,
                "model": self.model_name
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            raise
    
    def clear_collection(self):
        """Xóa toàn bộ collection"""
        try:
            self.chroma_client.delete_collection(name=self.collection_name)
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Military psychology Q&A database"}
            )
            logger.info("Collection cleared and recreated")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            raise
