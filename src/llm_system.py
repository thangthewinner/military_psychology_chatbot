"""
Module xử lý tương tác với LLM
"""
import os
from loguru import logger
from litellm import completion
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import GROQ_API_KEY, LLM_MODEL


# Thiết lập API key
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


class LLMSystem:
    """
    Hệ thống tương tác với LLM
    """
    
    def __init__(self, model_name=LLM_MODEL):
        """
        Khởi tạo LLMSystem
        
        Args:
            model_name (str): Tên mô hình LLM
        """
        self.model_name = model_name
        logger.info(f"Khởi tạo LLMSystem với mô hình {model_name}")
        
        # Kiểm tra API key
        if not GROQ_API_KEY:
            logger.warning("GROQ_API_KEY không được cấu hình, vui lòng kiểm tra file .env")
    
    def create_prompt_template(self):
        """
        Tạo template cho prompt
        
        Returns:
            PromptTemplate: Template cho prompt
        """
        template = """Bạn là một trợ lý tư vấn tâm lý chuyên nghiệp dành cho quân nhân trong quân đội Việt Nam.
Nhiệm vụ của bạn là cung cấp hỗ trợ tâm lý, lời khuyên và giải pháp cho các vấn đề mà quân nhân gặp phải.

Dưới đây là một số thông tin hữu ích từ cơ sở dữ liệu của chúng tôi:

{context}

Dựa trên thông tin trên, hãy trả lời câu hỏi sau một cách chuyên nghiệp, đồng cảm và hữu ích:

Câu hỏi: {question}

Trả lời:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def generate_response(self, question, context):
        """
        Tạo câu trả lời từ LLM
        
        Args:
            question (str): Câu hỏi của người dùng
            context (str): Ngữ cảnh từ vector database
        
        Returns:
            str: Câu trả lời từ LLM
        """
        try:
            logger.info(f"Tạo câu trả lời cho câu hỏi: {question}")
            
            # Tạo prompt
            prompt_template = self.create_prompt_template()
            prompt = prompt_template.format(
                context=context,
                question=question
            )
            
            # Gọi API LLM
            response = completion(
                model="groq/" + self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1024
            )
            
            # Xử lý kết quả
            answer = response.choices[0].message.content
            logger.info("Đã tạo câu trả lời thành công")
            
            return answer
        except Exception as e:
            logger.error(f"Lỗi khi tạo câu trả lời: {e}")
            return "Xin lỗi, tôi không thể trả lời câu hỏi của bạn lúc này. Vui lòng thử lại sau."
