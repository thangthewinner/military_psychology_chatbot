"""
Script để khởi tạo vector database
"""
from loguru import logger

from src.logger import setup_logger
from src.data_processor import DataProcessor
from src.embedding_system import EmbeddingSystem


def setup_database():
    """
    Khởi tạo vector database từ dữ liệu
    """
    logger.info("Bắt đầu khởi tạo vector database")
    
    try:
        # Tải và xử lý dữ liệu
        data_processor = DataProcessor()
        documents = data_processor.get_documents()
        
        if not documents:
            logger.error("Không có dữ liệu để tạo vector database")
            return False
        
        # Tạo vector database
        embedding_system = EmbeddingSystem()
        embedding_system.load_embeddings()
        embedding_system.create_vector_store(documents)
        
        # Lưu vector database
        result = embedding_system.save_vector_store()
        
        if result:
            logger.info("Đã khởi tạo vector database thành công")
            return True
        else:
            logger.error("Không thể lưu vector database")
            return False
    
    except Exception as e:
        logger.error(f"Lỗi khi khởi tạo vector database: {e}")
        return False


if __name__ == "__main__":
    # Thiết lập logger
    setup_logger()
    
    # Khởi tạo database
    success = setup_database()
    
    if success:
        print("Đã khởi tạo vector database thành công!")
    else:
        print("Khởi tạo vector database thất bại. Vui lòng kiểm tra logs để biết thêm chi tiết.")
