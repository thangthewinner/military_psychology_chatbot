"""
Module xử lý embedding và vector database
"""
import os
from pathlib import Path

import faiss
import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS as LangchainFAISS
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import EMBEDDING_MODEL, VECTOR_DB_PATH


class EmbeddingSystem:
    """
    Hệ thống quản lý embedding và vector database
    """
    
    def __init__(self, model_name=EMBEDDING_MODEL, vector_db_path=VECTOR_DB_PATH):
        """
        Khởi tạo EmbeddingSystem
        
        Args:
            model_name (str): Tên mô hình embedding
            vector_db_path (str): Đường dẫn lưu vector database
        """
        self.model_name = model_name
        self.vector_db_path = vector_db_path
        self.embeddings = None
        self.vector_store = None
        
        logger.info(f"Khởi tạo EmbeddingSystem với mô hình {model_name}")
        
        # Tạo thư mục vector_db nếu chưa tồn tại
        Path(vector_db_path).mkdir(exist_ok=True, parents=True)
    
    def load_embeddings(self):
        """
        Tải mô hình embedding
        
        Returns:
            HuggingFaceEmbeddings: Đối tượng embedding
        """
        try:
            logger.info(f"Đang tải mô hình embedding {self.model_name}")
            
            model_kwargs = {'device': 'cpu',
                            'trust_remote_code': True}
            encode_kwargs = {'normalize_embeddings': True}
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
            
            logger.info(f"Đã tải thành công mô hình embedding {self.model_name}")
            return self.embeddings
        except Exception as e:
            logger.error(f"Lỗi khi tải mô hình embedding: {e}")
            raise
    
    def create_vector_store(self, documents):
        """
        Tạo vector store từ documents
        
        Args:
            documents (list): Danh sách documents
        
        Returns:
            LangchainFAISS: Vector store
        """
        if self.embeddings is None:
            self.load_embeddings()
        
        try:
            logger.info("Bắt đầu tạo vector store")
            
            texts = [doc['content'] for doc in documents]
            metadatas = [doc['metadata'] for doc in documents]
            
            self.vector_store = LangchainFAISS.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )
            
            logger.info(f"Đã tạo thành công vector store với {len(texts)} documents")
            return self.vector_store
        except Exception as e:
            logger.error(f"Lỗi khi tạo vector store: {e}")
            raise
    
    def save_vector_store(self):
        """
        Lưu vector store
        """
        if self.vector_store is None:
            logger.error("Không thể lưu vector store vì chưa được khởi tạo")
            return False
        
        try:
            logger.info(f"Đang lưu vector store vào {self.vector_db_path}")
            self.vector_store.save_local(self.vector_db_path)
            logger.info("Đã lưu vector store thành công")
            return True
        except Exception as e:
            logger.error(f"Lỗi khi lưu vector store: {e}")
            return False
    
    def load_vector_store(self):
        """
        Tải vector store từ đĩa
        
        Returns:
            LangchainFAISS: Vector store đã tải
        """
        if self.embeddings is None:
            self.load_embeddings()
        
        try:
            if not os.path.exists(os.path.join(self.vector_db_path, "index.faiss")):
                logger.warning("Không tìm thấy vector store, cần tạo mới trước khi sử dụng")
                return None
            
            logger.info(f"Đang tải vector store từ {self.vector_db_path}")
            self.vector_store = LangchainFAISS.load_local(
                self.vector_db_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("Đã tải vector store thành công")
            return self.vector_store
        except Exception as e:
            logger.error(f"Lỗi khi tải vector store: {e}")
            return None
    
    def similarity_search(self, query, k=3):
        """
        Tìm kiếm các document tương tự với câu hỏi
        
        Args:
            query (str): Câu hỏi cần tìm
            k (int): Số lượng kết quả trả về
        
        Returns:
            list: Danh sách các document tương tự
        """
        if self.vector_store is None:
            self.load_vector_store()
            if self.vector_store is None:
                logger.error("Không thể thực hiện tìm kiếm vì vector store chưa được tạo")
                return []
        
        try:
            logger.info(f"Tìm kiếm {k} documents tương tự cho câu hỏi: {query}")
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Đã tìm thấy {len(results)} kết quả")
            return results
        except Exception as e:
            logger.error(f"Lỗi khi tìm kiếm: {e}")
            return []
