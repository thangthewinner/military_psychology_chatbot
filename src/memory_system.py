"""
Module quản lý memory cho chatbot
"""
from loguru import logger
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

class MemorySystem:
    """
    Hệ thống quản lý memory cho chatbot sử dụng ConversationBufferWindowMemory
    """
    
    def __init__(self, k=5):
        """
        Khởi tạo MemorySystem với ConversationBufferWindowMemory
        
        Args:
            k (int): Số lượng tin nhắn gần nhất được lưu trữ
        """
        self.chat_history = ChatMessageHistory()
        self.memory = ConversationBufferWindowMemory(
            chat_memory=self.chat_history,
            memory_key="chat_history",
            return_messages=True,
            k=k  # Chỉ lưu k tin nhắn gần nhất
        )
        
        logger.info(f"Khởi tạo MemorySystem với ConversationBufferWindowMemory (k={k})")
    
    def add_user_message(self, message):
        """
        Thêm tin nhắn của người dùng vào memory
        
        Args:
            message (str): Tin nhắn của người dùng
        """
        self.chat_history.add_user_message(message)
        logger.info(f"Đã thêm tin nhắn người dùng vào memory")
    
    def add_ai_message(self, message):
        """
        Thêm tin nhắn của AI vào memory
        
        Args:
            message (str): Tin nhắn của AI
        """
        self.chat_history.add_ai_message(message)
        logger.info(f"Đã thêm tin nhắn AI vào memory")
    
    def get_chat_history(self):
        """
        Lấy lịch sử chat từ memory
        
        Returns:
            str: Lịch sử chat được định dạng
        """
        messages = self.chat_history.messages
        formatted_history = ""
        
        for message in messages:
            if isinstance(message, HumanMessage):
                formatted_history += f"Người dùng: {message.content}\n\n"
            elif isinstance(message, AIMessage):
                formatted_history += f"Trợ lý: {message.content}\n\n"
        
        return formatted_history
    
    def get_memory_variables(self):
        """
        Lấy biến memory để sử dụng trong prompt
        
        Returns:
            dict: Biến memory
        """
        return self.memory.load_memory_variables({})
    
    def clear(self):
        """
        Xóa toàn bộ memory
        """
        self.chat_history.clear()
        logger.info("Đã xóa toàn bộ memory")
