import pandas as pd
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Xử lý dữ liệu từ file CSV"""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """Load dữ liệu từ file CSV"""
        try:
            self.data = pd.read_csv(self.data_file)
            logger.info(f"Loaded {len(self.data)} records from {self.data_file}")
            return self.data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def get_qa_pairs(self) -> List[Dict[str, str]]:
        """Lấy danh sách cặp câu hỏi-trả lời"""
        if self.data is None:
            self.load_data()
        
        qa_pairs = []
        for _, row in self.data.iterrows():
            qa_pairs.append({
                'question': row['question'],
                'answer': row['answer']
            })
        
        return qa_pairs
    
    def get_questions(self) -> List[str]:
        """Lấy danh sách câu hỏi"""
        if self.data is None:
            self.load_data()
        
        return self.data['question'].tolist()
    
    def get_answers(self) -> List[str]:
        """Lấy danh sách câu trả lời"""
        if self.data is None:
            self.load_data()
        
        return self.data['answer'].tolist()
    
    def get_documents_for_embedding(self) -> List[str]:
        """Tạo documents cho embedding (kết hợp question + answer)"""
        if self.data is None:
            self.load_data()
        
        documents = []
        for _, row in self.data.iterrows():
            # Kết hợp câu hỏi và trả lời để tạo document
            doc = f"Question: {row['question']}\nAnswer: {row['answer']}"
            documents.append(doc)
        
        return documents
    
    def get_metadata(self) -> List[Dict]:
        """Lấy metadata cho mỗi document"""
        if self.data is None:
            self.load_data()
        
        metadata = []
        for idx, row in self.data.iterrows():
            metadata.append({
                'id': idx,
                'question': row['question'],
                'answer': row['answer'],
                'type': 'military_psychology'
            })
        
        return metadata
