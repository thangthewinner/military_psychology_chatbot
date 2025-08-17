"""
Module quản lý chatbot
"""
from loguru import logger

from src.rag_system import RAGSystem
from src.history_manager import HistoryManager


class Chatbot:
    """
    Chatbot tư vấn tâm lý cho quân nhân
    """
    
    def __init__(self):
        """
        Khởi tạo Chatbot
        """
        self.rag_system = RAGSystem()
        self.conversation_history = []
        self.history_manager = HistoryManager()
        
        logger.info("Khởi tạo Chatbot")
    
    def setup(self):
        """
        Thiết lập chatbot
        """
        logger.info("Thiết lập Chatbot")
        return self.rag_system.setup()
    
    def add_message(self, role, content):
        """
        Thêm tin nhắn vào lịch sử hội thoại và lưu vào file CSV
        
        Args:
            role (str): Vai trò (user hoặc assistant)
            content (str): Nội dung tin nhắn
        """
        # Thêm vào conversation_history cho UI
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Lưu vào file CSV thông qua history_manager
        self.history_manager.save_message(role, content)
    
    def get_conversation_history(self):
        """
        Lấy lịch sử hội thoại
        
        Returns:
            list: Lịch sử hội thoại
        """
        return self.conversation_history
    
    def process_message(self, message):
        """
        Xử lý tin nhắn từ người dùng
        
        Args:
            message (str): Tin nhắn từ người dùng
        
        Returns:
            str: Câu trả lời từ chatbot
        """
        try:
            # Thêm tin nhắn vào lịch sử conversation_history (cho UI)
            self.add_message("user", message)
            
            # Xử lý câu hỏi
            logger.info(f"Xử lý tin nhắn từ người dùng: {message}")
            response = self.rag_system.process_query(message)
            
            # Thêm câu trả lời vào lịch sử conversation_history (cho UI)
            self.add_message("assistant", response)
            
            logger.info("Đã xử lý tin nhắn thành công")
            return response
        except Exception as e:
            logger.error(f"Lỗi khi xử lý tin nhắn: {e}")
            error_message = "Xin lỗi, đã xảy ra lỗi khi xử lý tin nhắn của bạn. Vui lòng thử lại sau."
            self.add_message("assistant", error_message)
            return error_message
            
    def process_message_stream(self, message):
        """
        Xử lý tin nhắn từ người dùng và trả về kết quả theo kiểu streaming
        
        Args:
            message (str): Tin nhắn từ người dùng
        
        Returns:
            generator: Generator trả về từng phần của câu trả lời
        """
        try:
            # Thêm tin nhắn vào lịch sử conversation_history (cho UI)
            self.add_message("user", message)
            
            # Xử lý câu hỏi streaming
            logger.info(f"Xử lý tin nhắn streaming từ người dùng: {message}")
            
            # Tạo biến để lưu toàn bộ câu trả lời
            full_response = ""
            
            # Trả về từng phần của câu trả lời
            # Lưu ý: memory đã được cập nhật trong RAGSystem
            for chunk in self.rag_system.process_query_stream(message):
                full_response += chunk
                yield chunk
            
            # Thêm câu trả lời đầy đủ vào lịch sử conversation_history (cho UI)
            self.add_message("assistant", full_response)
            
            logger.info("Đã xử lý tin nhắn streaming thành công")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý tin nhắn streaming: {e}")
            error_message = "Xin lỗi, đã xảy ra lỗi khi xử lý tin nhắn của bạn. Vui lòng thử lại sau."
            self.add_message("assistant", error_message)
            yield error_message
