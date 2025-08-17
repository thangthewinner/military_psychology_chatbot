"""
File chính để khởi động ứng dụng
"""
import os
import sys
import argparse
from loguru import logger

sys.path.append(os.path.abspath("."))
from src.logger import setup_logger


def parse_args():
    """
    Phân tích tham số dòng lệnh
    
    Returns:
        argparse.Namespace: Các tham số dòng lệnh
    """
    parser = argparse.ArgumentParser(description="Chatbot tư vấn tâm lý cho quân nhân")
    parser.add_argument(
        "--setup-db",
        action="store_true",
        help="Khởi tạo vector database"
    )
    parser.add_argument(
        "--run-app",
        action="store_true",
        help="Khởi động ứng dụng Streamlit"
    )
    
    return parser.parse_args()


def ensure_directories_exist():
    """
    Đảm bảo các thư mục cần thiết tồn tại
    """
    directories = ["logs", "history"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Đã tạo thư mục {directory}")
        else:
            logger.debug(f"Thư mục {directory} đã tồn tại")


def main():
    """
    Hàm chính của ứng dụng
    """
    # Thiết lập logger
    setup_logger()
    
    # Đảm bảo các thư mục cần thiết tồn tại
    ensure_directories_exist()
    
    # Phân tích tham số dòng lệnh
    args = parse_args()
    
    # Nếu không có tham số nào được cung cấp, hiển thị trợ giúp
    if not (args.setup_db or args.run_app):
        logger.info("Không có tham số nào được cung cấp, hiển thị trợ giúp")
        print("Sử dụng: python main.py [--setup-db] [--run-app]")
        print("  --setup-db: Khởi tạo vector database")
        print("  --run-app: Khởi động ứng dụng Streamlit")
        return
    
    # Khởi tạo vector database
    if args.setup_db:
        logger.info("Bắt đầu khởi tạo vector database")
        from src.database_setup import setup_database
        
        success = setup_database()
        
        if success:
            print("Đã khởi tạo vector database thành công!")
        else:
            print("Khởi tạo vector database thất bại. Vui lòng kiểm tra logs để biết thêm chi tiết.")
    
    # Khởi động ứng dụng Streamlit
    if args.run_app:
        logger.info("Bắt đầu khởi động ứng dụng Streamlit")
        
        try:
            # Khởi động Streamlit
            print("Đang khởi động ứng dụng Streamlit...")
            os.system("python -m streamlit run src/streamlit_app.py")
        
        except Exception as e:
            logger.error(f"Lỗi khi khởi động ứng dụng: {e}")
            print(f"Lỗi khi khởi động ứng dụng: {e}")


if __name__ == "__main__":
    main()
