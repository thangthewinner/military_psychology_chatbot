#!/usr/bin/env python3
"""
Chatbot Tư vấn Tâm lý Quân nhân
Main entry point for the application
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def check_environment():
    """Kiểm tra môi trường và dependencies"""
    logger = logging.getLogger(__name__)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        logger.warning("File .env không tồn tại. Vui lòng tạo file .env với GOOGLE_API_KEY")
        print("⚠️  Vui lòng tạo file .env với nội dung:")
        print("GOOGLE_API_KEY=your_google_api_key_here")
        print("EMBEDDING_MODEL=Alibaba-NLP/gte-multilingual-base")
        print("CHROMA_PERSIST_DIRECTORY=./chroma_db")
        return False
    
    # Check if data file exists
    if not os.path.exists('data/military_psychology.csv'):
        logger.error("File data/military_psychology.csv không tồn tại")
        return False
    
    # Check if src directory exists
    if not os.path.exists('src'):
        logger.error("Thư mục src không tồn tại")
        return False
    
    logger.info("✅ Môi trường đã sẵn sàng")
    return True

def main():
    """Main function"""
    print("🎖️  Chatbot Tư vấn Tâm lý Quân nhân")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("❌ Kiểm tra môi trường thất bại")
        return
    
    # Import and run Streamlit app
    try:
        import streamlit.web.cli as stcli
        import sys
        
        # Set up streamlit arguments
        sys.argv = [
            "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        print("🚀 Khởi động ứng dụng Streamlit...")
        stcli.main()
        
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("Vui lòng cài đặt dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Lỗi khởi động: {e}")

if __name__ == "__main__":
    main()
