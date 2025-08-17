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


def main():
    """
    Hàm chính của ứng dụng
    """
    # Thiết lập logger
    setup_logger()
    
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
            # Kiểm tra xem vector database đã được tạo chưa
            vector_db_path = os.path.join("vector_db", "index.faiss")
            if not os.path.exists(vector_db_path):
                print("CẢNH BÁO: Vector database chưa được khởi tạo. Vui lòng chạy 'python main.py --setup-db' trước.")
                logger.warning("Vector database chưa được khởi tạo")
            
            # Khởi động Streamlit
            print("Đang khởi động ứng dụng Streamlit...")
            os.system("python -m streamlit run src/streamlit_app.py")
        
        except Exception as e:
            logger.error(f"Lỗi khi khởi động ứng dụng: {e}")
            print(f"Lỗi khi khởi động ứng dụng: {e}")


if __name__ == "__main__":
    main()
