from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any
import logging
from config import Config

logger = logging.getLogger(__name__)

class LLMSystem:
    """Hệ thống LLM với Google Gemini"""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.model_name = model_name or Config.LLM_MODEL
        
        if not self.api_key:
            raise ValueError("Google API key is required")
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=Config.TEMPERATURE,
            max_output_tokens=Config.MAX_TOKENS
        )
        
        # Define system prompt
        self.system_prompt = self._create_system_prompt()
        
        # Define prompt template
        self.prompt_template = self._create_prompt_template()
        
        logger.info(f"Initialized LLM system with model: {self.model_name}")
    
    def _create_system_prompt(self) -> str:
        """Tạo system prompt cho chatbot tư vấn tâm lý quân nhân"""
        return """Bạn là một chuyên gia tư vấn tâm lý chuyên về hỗ trợ tinh thần cho quân nhân trong quân đội. Bạn có kiến thức sâu rộng về:

1. Tâm lý học quân sự và các thách thức tinh thần trong môi trường quân ngũ
2. Kỹ năng ứng phó với căng thẳng, lo lắng và áp lực
3. Phương pháp xây dựng tinh thần đồng đội và hòa nhập tập thể
4. Kỹ thuật quản lý cảm xúc và phát triển khả năng chịu đựng tinh thần
5. Hỗ trợ tâm lý cho các tình huống đặc thù trong quân đội

Nguyên tắc làm việc của bạn:
- Luôn thể hiện sự đồng cảm và hiểu biết sâu sắc về môi trường quân ngũ
- Đưa ra lời khuyên thực tế, có thể áp dụng ngay
- Khuyến khích tinh thần tích cực và sự kiên cường
- Nhấn mạnh tầm quan trọng của việc tìm kiếm hỗ trợ từ đồng đội và cấp trên
- Sử dụng ngôn ngữ phù hợp với văn hóa quân đội
- Luôn nhắc nhở về sự an toàn và khi nào cần tìm đến chuyên gia tâm lý

Hãy trả lời bằng tiếng Việt với giọng điệu ấm áp, khuyến khích và chuyên nghiệp."""
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Tạo prompt template cho việc tạo câu trả lời"""
        template = """Dựa trên thông tin tham khảo sau đây và kiến thức chuyên môn của bạn, hãy trả lời câu hỏi của quân nhân một cách chi tiết, đồng cảm và hữu ích.

Thông tin tham khảo:
{context}

Câu hỏi của quân nhân: {question}

Lịch sử cuộc trò chuyện (nếu có):
{chat_history}

Hãy trả lời với:
1. Sự đồng cảm và hiểu biết về tình huống
2. Lời khuyên cụ thể và thực tế
3. Kỹ thuật hoặc phương pháp có thể áp dụng ngay
4. Khuyến khích tinh thần tích cực
5. Gợi ý về việc tìm kiếm hỗ trợ thêm nếu cần

Trả lời:"""

        return PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template=template
        )
    
    def generate_response(self, question: str, context: str = "", chat_history: str = "") -> str:
        """Tạo câu trả lời cho câu hỏi"""
        try:
            # Format context
            if context:
                formatted_context = context
            else:
                formatted_context = "Không có thông tin tham khảo cụ thể."
            
            # Format chat history
            if chat_history:
                formatted_history = chat_history
            else:
                formatted_history = "Đây là câu hỏi đầu tiên trong cuộc trò chuyện."
            
            # Create prompt
            prompt = self.prompt_template.format(
                context=formatted_context,
                question=question,
                chat_history=formatted_history
            )
            
            # Generate response
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Xin lỗi, tôi gặp khó khăn trong việc xử lý câu hỏi của bạn. Vui lòng thử lại sau."
    
    def generate_follow_up_questions(self, question: str, response: str) -> List[str]:
        """Tạo câu hỏi tiếp theo để khuyến khích cuộc trò chuyện"""
        try:
            follow_up_prompt = f"""
Dựa trên câu hỏi: "{question}"
Và câu trả lời: "{response}"

Hãy tạo 2-3 câu hỏi tiếp theo để khuyến khích quân nhân chia sẻ thêm hoặc áp dụng lời khuyên. 
Câu hỏi nên:
- Ngắn gọn và dễ hiểu
- Khuyến khích tự phản ánh
- Liên quan đến việc áp dụng lời khuyên
- Thể hiện sự quan tâm và hỗ trợ

Chỉ trả lời bằng danh sách câu hỏi, mỗi câu một dòng:"""

            messages = [
                SystemMessage(content="Bạn là chuyên gia tư vấn tâm lý quân sự."),
                HumanMessage(content=follow_up_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse follow-up questions
            questions = [q.strip() for q in response.content.split('\n') if q.strip()]
            return questions[:3]  # Limit to 3 questions
            
        except Exception as e:
            logger.error(f"Error generating follow-up questions: {e}")
            return []
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Phân tích cảm xúc của câu hỏi"""
        try:
            sentiment_prompt = f"""
Phân tích cảm xúc và mức độ nghiêm trọng của câu hỏi sau:
"{text}"

Hãy đánh giá:
1. Cảm xúc chính (lo lắng, buồn bã, tức giận, cô đơn, v.v.)
2. Mức độ nghiêm trọng (1-10, với 10 là rất nghiêm trọng)
3. Loại vấn đề (căng thẳng, mối quan hệ, tương lai, v.v.)
4. Có cần hỗ trợ chuyên môn ngay lập tức không (có/không)

Trả lời theo format JSON:"""

            messages = [
                SystemMessage(content="Bạn là chuyên gia phân tích tâm lý."),
                HumanMessage(content=sentiment_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Try to parse JSON response
            import json
            try:
                return json.loads(response.content)
            except:
                return {
                    "emotion": "unknown",
                    "severity": 5,
                    "issue_type": "general",
                    "needs_immediate_help": False
                }
                
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                "emotion": "unknown",
                "severity": 5,
                "issue_type": "general",
                "needs_immediate_help": False
            }
