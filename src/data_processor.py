"""
Module xử lý dữ liệu cho chatbot
"""
import pandas as pd
from loguru import logger

from src.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP


class DataProcessor:
    """
    Xử lý dữ liệu câu hỏi và câu trả lời cho chatbot
    """
    
    def __init__(self, data_path=DATA_PATH):
        """
        Khởi tạo DataProcessor
        
        Args:
            data_path (str): Đường dẫn đến file dữ liệu CSV
        """
        self.data_path = data_path
        logger.info(f"Khởi tạo DataProcessor với dữ liệu từ {data_path}")
    
    def load_data(self):
        """
        Đọc dữ liệu từ file CSV
        
        Returns:
            pd.DataFrame: DataFrame chứa dữ liệu câu hỏi và câu trả lời
        """
        try:
            logger.info(f"Đang đọc dữ liệu từ {self.data_path}")
            df = pd.read_csv(self.data_path)
            logger.info(f"Đã đọc thành công {len(df)} bản ghi")
            return df
        except Exception as e:
            logger.error(f"Lỗi khi đọc dữ liệu: {e}")
            raise
    
    def preprocess_data(self, df=None):
        """
        Tiền xử lý dữ liệu
        
        Args:
            df (pd.DataFrame, optional): DataFrame cần xử lý. Nếu None, sẽ tự động load dữ liệu.
            
        Returns:
            pd.DataFrame: DataFrame đã được xử lý
        """
        if df is None:
            df = self.load_data()
        
        logger.info("Bắt đầu tiền xử lý dữ liệu")
        
        # Kiểm tra và xử lý dữ liệu thiếu
        if df['question'].isna().sum() > 0 or df['answer'].isna().sum() > 0:
            logger.warning(f"Phát hiện {df['question'].isna().sum()} câu hỏi và {df['answer'].isna().sum()} câu trả lời bị thiếu")
            df = df.dropna(subset=['question', 'answer'])
            logger.info(f"Đã loại bỏ các bản ghi thiếu dữ liệu, còn lại {len(df)} bản ghi")
        
        # Tạo trường context để sử dụng cho embedding
        df['context'] = "Câu hỏi: " + df['question'] + "\nCâu trả lời: " + df['answer']
        
        logger.info("Hoàn thành tiền xử lý dữ liệu")
        return df
    
    def get_documents(self):
        """
        Lấy danh sách documents để tạo vector embeddings
        
        Returns:
            list: Danh sách các document
        """
        df = self.preprocess_data()
        
        documents = []
        for _, row in df.iterrows():
            documents.append({
                'content': row['context'],
                'metadata': {
                    'question': row['question'],
                    'answer': row['answer']
                }
            })
        
        logger.info(f"Đã tạo {len(documents)} documents cho embedding")
        return documents
