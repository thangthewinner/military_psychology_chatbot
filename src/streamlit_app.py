"""
Giao diện người dùng Streamlit cho chatbot
"""
import streamlit as st
from loguru import logger

import sys
import os

# Thêm thư mục gốc vào sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logger import setup_logger
from src.chatbot import Chatbot
from src.config import STREAMLIT_TITLE, STREAMLIT_DESCRIPTION


def initialize_session_state():
    """
    Khởi tạo session state
    """
    if "chatbot" not in st.session_state:
        logger.info("Khởi tạo chatbot trong session state")
        st.session_state.chatbot = Chatbot()
        setup_success = st.session_state.chatbot.setup()
        
        if not setup_success:
            st.error("Không thể khởi tạo chatbot. Vui lòng kiểm tra logs để biết thêm chi tiết.")
            logger.error("Không thể khởi tạo chatbot trong session state")
    
    if "messages" not in st.session_state:
        logger.info("Khởi tạo lịch sử tin nhắn trong session state")
        st.session_state.messages = []


def display_chat_history():
    """
    Hiển thị lịch sử chat
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    """
    Hàm chính của ứng dụng Streamlit
    """
    # Thiết lập logger
    setup_logger()
    
    # Thiết lập trang
    st.set_page_config(
        page_title=STREAMLIT_TITLE,
        page_icon="🪖",
        layout="wide"
    )
    
    # Layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("## Hướng dẫn sử dụng")
        st.markdown("""
        ### Chatbot Tư Vấn Tâm Lý Quân Nhân
        
        Chatbot này được thiết kế để hỗ trợ tư vấn tâm lý cho quân nhân trong quân đội.
        
        **Cách sử dụng:**
        1. Nhập câu hỏi hoặc vấn đề tâm lý bạn đang gặp phải vào ô nhập liệu
        2. Nhấn Enter hoặc nút gửi để nhận câu trả lời
        3. Chatbot sẽ phân tích và đưa ra lời khuyên dựa trên cơ sở dữ liệu tâm lý quân sự
        
        **Lưu ý:**
        - Đây là công cụ hỗ trợ, không thay thế hoàn toàn chuyên gia tâm lý
        - Trong trường hợp khẩn cấp, vui lòng liên hệ trực tiếp với cán bộ tâm lý đơn vị
        """)
    
    with col2:
        # Tiêu đề
        st.title(STREAMLIT_TITLE)
        st.markdown(STREAMLIT_DESCRIPTION)
        
        # Khởi tạo session state
        initialize_session_state()
        
        # Hiển thị lịch sử chat
        display_chat_history()
        
        # Nhập tin nhắn mới
        if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
            logger.info(f"Người dùng nhập: {prompt}")
            
            # Hiển thị tin nhắn của người dùng
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Xử lý câu trả lời
            with st.chat_message("assistant"):
                with st.spinner("Đang suy nghĩ..."):
                    try:
                        response = st.session_state.chatbot.process_message(prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        logger.info("Đã hiển thị câu trả lời")
                    except Exception as e:
                        error_message = "Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi của bạn. Vui lòng thử lại sau."
                        st.markdown(error_message)
                        st.session_state.messages.append({"role": "assistant", "content": error_message})
                        logger.error(f"Lỗi khi xử lý câu trả lời: {e}")


if __name__ == "__main__":
    main()
