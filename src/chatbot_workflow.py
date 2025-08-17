from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Dict, List, Any, TypedDict, Annotated
import logging
from src.embedding_system import EmbeddingSystem
from src.llm_system import LLMSystem
from src.data_processor import DataProcessor
from config import Config

logger = logging.getLogger(__name__)

# Define state structure
class ChatState(TypedDict):
    question: str
    context: str
    response: str
    chat_history: List[Dict[str, str]]
    sentiment: Dict[str, Any]
    follow_up_questions: List[str]
    error: str
    needs_immediate_help: bool

class ChatbotWorkflow:
    """Workflow thông minh cho chatbot sử dụng LangGraph"""
    
    def __init__(self):
        # Initialize components
        self.embedding_system = EmbeddingSystem()
        self.llm_system = LLMSystem()
        self.data_processor = DataProcessor(Config.DATA_FILE)
        
        # Initialize workflow
        self.workflow = self._create_workflow()
        
        logger.info("Chatbot workflow initialized")
    
    def _create_workflow(self) -> StateGraph:
        """Tạo workflow graph"""
        
        # Create state graph
        workflow = StateGraph(ChatState)
        
        # Add nodes
        workflow.add_node("analyze_sentiment", self._analyze_sentiment_node)
        workflow.add_node("retrieve_context", self._retrieve_context_node)
        workflow.add_node("generate_response", self._generate_response_node)
        workflow.add_node("generate_follow_up", self._generate_follow_up_node)
        workflow.add_node("check_emergency", self._check_emergency_node)
        
        # Add edges
        workflow.add_edge("analyze_sentiment", "retrieve_context")
        workflow.add_edge("retrieve_context", "generate_response")
        workflow.add_edge("generate_response", "generate_follow_up")
        workflow.add_edge("generate_follow_up", "check_emergency")
        workflow.add_edge("check_emergency", END)
        
        # Set entry point
        workflow.set_entry_point("analyze_sentiment")
        
        return workflow.compile()
    
    def _analyze_sentiment_node(self, state: ChatState) -> ChatState:
        """Phân tích cảm xúc của câu hỏi"""
        try:
            question = state["question"]
            sentiment = self.llm_system.analyze_sentiment(question)
            
            state["sentiment"] = sentiment
            state["needs_immediate_help"] = sentiment.get("needs_immediate_help", False)
            
            logger.info(f"Sentiment analyzed: {sentiment}")
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            state["error"] = f"Sentiment analysis error: {str(e)}"
            state["sentiment"] = {
                "emotion": "unknown",
                "severity": 5,
                "issue_type": "general",
                "needs_immediate_help": False
            }
        
        return state
    
    def _retrieve_context_node(self, state: ChatState) -> ChatState:
        """Tìm kiếm context liên quan"""
        try:
            question = state["question"]
            
            # Search for relevant context
            search_results = self.embedding_system.search_by_text(question)
            
            if search_results and search_results.get("documents"):
                # Combine relevant documents
                documents = search_results["documents"][0]  # First query results
                context = "\n\n".join(documents)
                state["context"] = context
            else:
                state["context"] = ""
            
            logger.info(f"Retrieved context with {len(documents) if 'documents' in search_results else 0} documents")
            
        except Exception as e:
            logger.error(f"Error in context retrieval: {e}")
            state["error"] = f"Context retrieval error: {str(e)}"
            state["context"] = ""
        
        return state
    
    def _generate_response_node(self, state: ChatState) -> ChatState:
        """Tạo câu trả lời"""
        try:
            question = state["question"]
            context = state["context"]
            
            # Format chat history
            chat_history = ""
            if state.get("chat_history"):
                history_texts = []
                for msg in state["chat_history"][-3:]:  # Last 3 messages
                    history_texts.append(f"Q: {msg['question']}\nA: {msg['response']}")
                chat_history = "\n\n".join(history_texts)
            
            # Generate response
            response = self.llm_system.generate_response(
                question=question,
                context=context,
                chat_history=chat_history
            )
            
            state["response"] = response
            
            logger.info("Response generated successfully")
            
        except Exception as e:
            logger.error(f"Error in response generation: {e}")
            state["error"] = f"Response generation error: {str(e)}"
            state["response"] = "Xin lỗi, tôi gặp khó khăn trong việc xử lý câu hỏi của bạn. Vui lòng thử lại sau."
        
        return state
    
    def _generate_follow_up_node(self, state: ChatState) -> ChatState:
        """Tạo câu hỏi tiếp theo"""
        try:
            question = state["question"]
            response = state["response"]
            
            # Generate follow-up questions
            follow_up_questions = self.llm_system.generate_follow_up_questions(
                question=question,
                response=response
            )
            
            state["follow_up_questions"] = follow_up_questions
            
            logger.info(f"Generated {len(follow_up_questions)} follow-up questions")
            
        except Exception as e:
            logger.error(f"Error in follow-up generation: {e}")
            state["follow_up_questions"] = []
        
        return state
    
    def _check_emergency_node(self, state: ChatState) -> ChatState:
        """Kiểm tra tình huống khẩn cấp"""
        try:
            sentiment = state.get("sentiment", {})
            severity = sentiment.get("severity", 5)
            
            # Check if immediate help is needed
            if severity >= 8 or state.get("needs_immediate_help", False):
                emergency_message = """
⚠️ LƯU Ý QUAN TRỌNG:
Dựa trên câu hỏi của bạn, tôi khuyến nghị bạn nên tìm kiếm sự hỗ trợ chuyên môn ngay lập tức. 
Vui lòng liên hệ với:
- Cán bộ tâm lý trong đơn vị
- Bác sĩ quân y
- Cấp trên trực tiếp
- Đường dây nóng hỗ trợ tâm lý quân đội

Bạn không đơn độc và luôn có người sẵn sàng lắng nghe và hỗ trợ bạn.
"""
                state["response"] = emergency_message + "\n\n" + state["response"]
            
            logger.info(f"Emergency check completed. Severity: {severity}")
            
        except Exception as e:
            logger.error(f"Error in emergency check: {e}")
        
        return state
    
    def process_message(self, question: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Xử lý tin nhắn qua workflow"""
        try:
            # Prepare initial state
            initial_state = ChatState(
                question=question,
                context="",
                response="",
                chat_history=chat_history or [],
                sentiment={},
                follow_up_questions=[],
                error="",
                needs_immediate_help=False
            )
            
            # Execute workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Update chat history
            if chat_history is None:
                chat_history = []
            
            chat_history.append({
                "question": question,
                "response": final_state["response"]
            })
            
            # Prepare result
            result = {
                "response": final_state["response"],
                "context": final_state["context"],
                "sentiment": final_state["sentiment"],
                "follow_up_questions": final_state["follow_up_questions"],
                "chat_history": chat_history,
                "error": final_state.get("error", ""),
                "needs_immediate_help": final_state.get("needs_immediate_help", False)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in workflow execution: {e}")
            return {
                "response": "Xin lỗi, hệ thống gặp lỗi. Vui lòng thử lại sau.",
                "context": "",
                "sentiment": {},
                "follow_up_questions": [],
                "chat_history": chat_history or [],
                "error": str(e),
                "needs_immediate_help": False
            }
    
    def initialize_database(self):
        """Khởi tạo database với dữ liệu từ CSV"""
        try:
            # Load data
            data_processor = DataProcessor(Config.DATA_FILE)
            documents = data_processor.get_documents_for_embedding()
            metadata = data_processor.get_metadata()
            
            # Clear existing collection
            self.embedding_system.clear_collection()
            
            # Add documents to database
            self.embedding_system.add_documents(
                documents=documents,
                metadata=metadata
            )
            
            logger.info(f"Database initialized with {len(documents)} documents")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
