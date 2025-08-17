"""
Module xử lý hệ thống RAG (Retrieval Augmented Generation)
"""
from loguru import logger
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.embedding_system import EmbeddingSystem
from src.llm_system import LLMSystem
from src.config import TOP_K


class RAGSystem:
    """
    Hệ thống RAG kết hợp retrieval và generation
    """
    
    def __init__(self):
        """
        Khởi tạo RAGSystem
        """
        self.embedding_system = EmbeddingSystem()
        self.llm_system = LLMSystem()
        self.chain = None
        
        # Thêm memory system
        from src.memory_system import MemorySystem
        self.memory_system = MemorySystem(k=5)  # Lưu 5 tin nhắn gần nhất
        
        logger.info("Khởi tạo RAGSystem")
    
    def setup(self):
        """
        Thiết lập hệ thống RAG
        """
        # Tải vector store
        vector_store = self.embedding_system.load_vector_store()
        if vector_store is None:
            logger.error("Không thể thiết lập RAG vì vector store chưa được tạo")
            return False
        
        # Tạo retriever
        retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K})
        
        # Tạo prompt template
        prompt_template = self.llm_system.create_prompt_template()
        
        # Hàm format context
        def format_docs(docs):
            return "\n\n".join([doc.page_content for doc in docs])
        
        # Tạo chain
        self.chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template
            | self.llm_system.generate_response
        )
        
        logger.info("Đã thiết lập RAG thành công")
        return True
    
    def process_query(self, query):
        """
        Xử lý câu hỏi từ người dùng
        
        Args:
            query (str): Câu hỏi của người dùng
        
        Returns:
            str: Câu trả lời
        """
        try:
            logger.info(f"Xử lý câu hỏi: {query}")
            
            # Lấy lịch sử hội thoại từ memory
            chat_history = self.memory_system.get_chat_history()
            
            # Tìm kiếm documents tương tự
            docs = self.embedding_system.similarity_search(query, k=TOP_K)
            
            if not docs:
                logger.warning("Không tìm thấy documents tương tự")
                return "Xin lỗi, tôi không có đủ thông tin để trả lời câu hỏi của bạn."
            
            # Format context
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Tạo câu trả lời với lịch sử hội thoại
            response = self.llm_system.generate_response(query, context, chat_history)
            
            # Cập nhật memory
            self.memory_system.add_user_message(query)
            self.memory_system.add_ai_message(response)
            
            logger.info("Đã xử lý câu hỏi thành công")
            return response
        except Exception as e:
            logger.error(f"Lỗi khi xử lý câu hỏi: {e}")
            return "Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi của bạn. Vui lòng thử lại sau."
            
    def process_query_stream(self, query):
        """
        Xử lý câu hỏi từ người dùng và trả về kết quả theo kiểu streaming
        
        Args:
            query (str): Câu hỏi của người dùng
        
        Returns:
            generator: Generator trả về từng phần của câu trả lời
        """
        try:
            logger.info(f"Xử lý câu hỏi streaming: {query}")
            
            # Lấy lịch sử hội thoại từ memory
            chat_history = self.memory_system.get_chat_history()
            
            # Tìm kiếm documents tương tự
            docs = self.embedding_system.similarity_search(query, k=TOP_K)
            
            if not docs:
                logger.warning("Không tìm thấy documents tương tự")
                yield "Xin lỗi, tôi không có đủ thông tin để trả lời câu hỏi của bạn."
                return
            
            # Format context
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Tạo câu trả lời streaming với lịch sử hội thoại
            full_response = ""
            for chunk in self.llm_system.generate_response_stream(query, context, chat_history):
                full_response += chunk
                yield chunk
            
            # Cập nhật memory sau khi hoàn thành
            self.memory_system.add_user_message(query)
            self.memory_system.add_ai_message(full_response)
            
            logger.info("Đã xử lý câu hỏi streaming thành công")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý câu hỏi streaming: {e}")
            yield "Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi của bạn. Vui lòng thử lại sau."
