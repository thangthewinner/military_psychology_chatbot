import streamlit as st
import logging
import json
from datetime import datetime
from src.chatbot_workflow import ChatbotWorkflow
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5a8b 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f4e79;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .bot-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .emergency-message {
        background-color: #ffebee;
        border-left-color: #f44336;
        border: 2px solid #f44336;
    }
    
    .follow-up-question {
        background-color: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .follow-up-question:hover {
        background-color: #c8e6c9;
    }
    
    .sentiment-indicator {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .severity-low { background-color: #c8e6c9; color: #2e7d32; }
    .severity-medium { background-color: #fff3e0; color: #ef6c00; }
    .severity-high { background-color: #ffebee; color: #c62828; }
    
    .sidebar-section {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'database_initialized' not in st.session_state:
    st.session_state.database_initialized = False

def initialize_chatbot():
    """Khởi tạo chatbot"""
    try:
        with st.spinner("Đang khởi tạo chatbot..."):
            chatbot = ChatbotWorkflow()
            
            # Initialize database if not done
            if not st.session_state.database_initialized:
                with st.spinner("Đang khởi tạo cơ sở dữ liệu..."):
                    chatbot.initialize_database()
                    st.session_state.database_initialized = True
            
            st.session_state.chatbot = chatbot
            st.success("Chatbot đã sẵn sàng!")
            
    except Exception as e:
        st.error(f"Lỗi khởi tạo chatbot: {str(e)}")
        logger.error(f"Chatbot initialization error: {e}")

def get_severity_class(severity):
    """Lấy CSS class cho mức độ nghiêm trọng"""
    if severity <= 3:
        return "severity-low"
    elif severity <= 7:
        return "severity-medium"
    else:
        return "severity-high"

def display_sentiment(sentiment):
    """Hiển thị thông tin cảm xúc"""
    if not sentiment:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        emotion = sentiment.get('emotion', 'unknown')
        st.metric("Cảm xúc", emotion.title())
    
    with col2:
        severity = sentiment.get('severity', 5)
        severity_class = get_severity_class(severity)
        st.markdown(f'<div class="sentiment-indicator {severity_class}">Mức độ: {severity}/10</div>', 
                   unsafe_allow_html=True)
    
    with col3:
        issue_type = sentiment.get('issue_type', 'general')
        st.metric("Loại vấn đề", issue_type.title())

def display_follow_up_questions(questions):
    """Hiển thị câu hỏi tiếp theo"""
    if not questions:
        return
    
    st.markdown("**Câu hỏi gợi ý:**")
    for i, question in enumerate(questions):
        if st.button(f"💭 {question}", key=f"follow_up_{i}"):
            st.session_state.user_input = question
            st.rerun()

def export_chat_history():
    """Xuất lịch sử chat"""
    if not st.session_state.chat_history:
        return None
    
    export_data = {
        "export_time": datetime.now().isoformat(),
        "chat_history": st.session_state.chat_history
    }
    
    return json.dumps(export_data, ensure_ascii=False, indent=2)

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎖️ Chatbot Tư vấn Tâm lý Quân nhân</h1>
        <p>Hỗ trợ tinh thần và tư vấn tâm lý cho quân nhân trong quân đội</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Cài đặt")
        
        # Initialize chatbot button
        if st.button("🚀 Khởi tạo Chatbot", type="primary"):
            initialize_chatbot()
        
        # Status
        st.markdown("### 📊 Trạng thái")
        if st.session_state.chatbot:
            st.success("✅ Chatbot đã sẵn sàng")
        else:
            st.warning("⚠️ Chatbot chưa được khởi tạo")
        
        if st.session_state.database_initialized:
            st.success("✅ Cơ sở dữ liệu đã sẵn sàng")
        else:
            st.warning("⚠️ Cơ sở dữ liệu chưa được khởi tạo")
        
        # Chat history info
        st.markdown("### 💬 Thông tin chat")
        st.metric("Số tin nhắn", len(st.session_state.chat_history))
        
        # Export chat history
        if st.session_state.chat_history:
            export_data = export_chat_history()
            st.download_button(
                label="📥 Xuất lịch sử chat",
                data=export_data,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Clear chat history
        if st.button("🗑️ Xóa lịch sử chat"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Help section
        st.markdown("### ❓ Hướng dẫn")
        st.markdown("""
        **Cách sử dụng:**
        1. Nhấn "Khởi tạo Chatbot" để bắt đầu
        2. Nhập câu hỏi của bạn vào ô chat
        3. Nhấn Enter hoặc nút gửi
        4. Chatbot sẽ phân tích và đưa ra lời khuyên
        
        **Lưu ý:** 
        - Chatbot chỉ hỗ trợ tư vấn tâm lý cơ bản
        - Với vấn đề nghiêm trọng, vui lòng tìm đến chuyên gia
        """)
        
        # Emergency contacts
        st.markdown("### 🆘 Liên hệ khẩn cấp")
        st.markdown("""
        **Khi cần hỗ trợ ngay lập tức:**
        - Cán bộ tâm lý đơn vị
        - Bác sĩ quân y
        - Cấp trên trực tiếp
        - Đường dây nóng tâm lý quân đội
        """)

    # Main chat area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat messages
        st.markdown("### 💬 Cuộc trò chuyện")
        
        # Display chat history
        for i, message in enumerate(st.session_state.chat_history):
            if message.get('is_emergency'):
                st.markdown(f"""
                <div class="chat-message emergency-message">
                    <strong>⚠️ CẢNH BÁO:</strong><br>
                    {message['response']}
                </div>
                """, unsafe_allow_html=True)
            else:
                # User message
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>Bạn:</strong><br>
                    {message['question']}
                </div>
                """, unsafe_allow_html=True)
                
                # Bot message
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>Chatbot:</strong><br>
                    {message['response']}
                </div>
                """, unsafe_allow_html=True)
                
                # Display sentiment if available
                if 'sentiment' in message and message['sentiment']:
                    with st.expander("📊 Phân tích cảm xúc"):
                        display_sentiment(message['sentiment'])
                
                # Display follow-up questions
                if 'follow_up_questions' in message and message['follow_up_questions']:
                    display_follow_up_questions(message['follow_up_questions'])
        
        # Input area
        st.markdown("### 💭 Nhập câu hỏi")
        
        # Initialize user_input in session state
        if 'user_input' not in st.session_state:
            st.session_state.user_input = ""
        
        # Text input
        user_input = st.text_area(
            "Nhập câu hỏi của bạn:",
            value=st.session_state.user_input,
            height=100,
            placeholder="Ví dụ: Tôi cảm thấy căng thẳng sau mỗi buổi huấn luyện..."
        )
        
        # Send button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("📤 Gửi", type="primary"):
                if user_input.strip() and st.session_state.chatbot:
                    # Process message
                    with st.spinner("Đang xử lý..."):
                        result = st.session_state.chatbot.process_message(
                            user_input, 
                            st.session_state.chat_history
                        )
                    
                    # Add to chat history
                    chat_message = {
                        'question': user_input,
                        'response': result['response'],
                        'sentiment': result['sentiment'],
                        'follow_up_questions': result['follow_up_questions'],
                        'is_emergency': result.get('needs_immediate_help', False)
                    }
                    
                    st.session_state.chat_history.append(chat_message)
                    st.session_state.user_input = ""
                    st.rerun()
                elif not st.session_state.chatbot:
                    st.error("Vui lòng khởi tạo chatbot trước!")
                elif not user_input.strip():
                    st.warning("Vui lòng nhập câu hỏi!")
        
        with col2:
            if st.button("🗑️ Xóa"):
                st.session_state.user_input = ""
                st.rerun()
    
    with col2:
        # System info
        st.markdown("### 🔧 Thông tin hệ thống")
        
        if st.session_state.chatbot:
            # Database info
            try:
                db_info = st.session_state.chatbot.embedding_system.get_collection_info()
                st.metric("Documents trong DB", db_info['document_count'])
                st.metric("Model embedding", db_info['model'].split('/')[-1])
            except:
                st.warning("Không thể lấy thông tin DB")
        
        # Recent activity
        st.markdown("### 📈 Hoạt động gần đây")
        if st.session_state.chat_history:
            recent_messages = st.session_state.chat_history[-3:]
            for msg in recent_messages:
                st.markdown(f"**Q:** {msg['question'][:50]}...")
                if 'sentiment' in msg and msg['sentiment']:
                    severity = msg['sentiment'].get('severity', 5)
                    st.markdown(f"*Mức độ: {severity}/10*")
                st.divider()
        else:
            st.info("Chưa có hoạt động nào")

if __name__ == "__main__":
    main()
