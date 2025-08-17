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
            
            # Tìm kiếm documents tương tự
            docs = self.embedding_system.similarity_search(query, k=TOP_K)
            
            if not docs:
                logger.warning("Không tìm thấy documents tương tự")
                return "Xin lỗi, tôi không có đủ thông tin để trả lời câu hỏi của bạn."
            
            # Format context
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Tạo câu trả lời
            response = self.llm_system.generate_response(query, context)
            
            logger.info("Đã xử lý câu hỏi thành công")
            return response
        except Exception as e:
            logger.error(f"Lỗi khi xử lý câu hỏi: {e}")
            return "Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi của bạn. Vui lòng thử lại sau."
