"""
Module quản lý lịch sử hội thoại
"""
import os
import uuid
import pandas as pd
from datetime import datetime
from pathlib import Path
from loguru import logger

class HistoryManager:
    """
    Quản lý lịch sử hội thoại và lưu trữ vào file CSV
    """
    
    def __init__(self, history_folder=None):
        """
        Khởi tạo HistoryManager
        
        Args:
            history_folder (str, optional): Thư mục lưu trữ lịch sử
        """
        from src.config import HISTORY_FOLDER
        self.history_folder = history_folder or HISTORY_FOLDER
        self.session_id = str(uuid.uuid4())[:8]  # Tạo session ID ngắn
        # Sử dụng múi giờ hiện tại
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.history_file = os.path.join(self.history_folder, f"{self.current_date}.csv")
        
        # Tạo thư mục history nếu chưa tồn tại
        Path(self.history_folder).mkdir(exist_ok=True)
        
        logger.info(f"Khởi tạo HistoryManager với session ID: {self.session_id}")
    
    def save_message(self, role, content):
        """
        Lưu tin nhắn vào file CSV
        
        Args:
            role (str): Vai trò (user hoặc assistant)
            content (str): Nội dung tin nhắn
        """
        # Tạo DataFrame cho tin nhắn mới với múi giờ hiện tại
        new_data = pd.DataFrame({
            'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'session_id': [self.session_id],
            'role': [role],
            'content': [content]
        })
        
        try:
            # Kiểm tra file đã tồn tại chưa
            if os.path.exists(self.history_file):
                # Đọc file hiện tại và thêm dữ liệu mới
                existing_data = pd.read_csv(self.history_file)
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            else:
                updated_data = new_data
            
            # Lưu vào file CSV
            updated_data.to_csv(self.history_file, index=False)
            logger.info(f"Đã lưu tin nhắn của {role} vào {self.history_file}")
        
        except Exception as e:
            logger.error(f"Lỗi khi lưu tin nhắn vào file CSV: {e}")
    
    def get_session_history(self, session_id=None):
        """
        Lấy lịch sử hội thoại của một session
        
        Args:
            session_id (str, optional): ID của session. Nếu None, sẽ lấy session hiện tại.
        
        Returns:
            list: Danh sách các tin nhắn trong session
        """
        if session_id is None:
            session_id = self.session_id
        
        try:
            if os.path.exists(self.history_file):
                data = pd.read_csv(self.history_file)
                session_data = data[data['session_id'] == session_id]
                
                # Chuyển đổi thành danh sách tin nhắn
                messages = []
                for _, row in session_data.iterrows():
                    messages.append({
                        'timestamp': row['timestamp'],
                        'role': row['role'],
                        'content': row['content']
                    })
                
                return messages
            else:
                return []
        
        except Exception as e:
            logger.error(f"Lỗi khi đọc lịch sử session: {e}")
            return []
    
    def get_all_sessions(self, date=None):
        """
        Lấy danh sách tất cả các session trong một ngày
        
        Args:
            date (str, optional): Ngày cần lấy (định dạng YYYY-MM-DD). Nếu None, sẽ lấy ngày hiện tại.
        
        Returns:
            list: Danh sách các session ID
        """
        if date is None:
            date = self.current_date
        
        history_file = os.path.join(self.history_folder, f"{date}.csv")
        
        try:
            if os.path.exists(history_file):
                data = pd.read_csv(history_file)
                return data['session_id'].unique().tolist()
            else:
                return []
        
        except Exception as e:
            logger.error(f"Lỗi khi lấy danh sách session: {e}")
            return []
    
    def create_new_session(self):
        """
        Tạo session mới
        
        Returns:
            str: ID của session mới
        """
        self.session_id = str(uuid.uuid4())[:8]
        logger.info(f"Đã tạo session mới với ID: {self.session_id}")
        return self.session_id
