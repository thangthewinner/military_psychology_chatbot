"""
Cấu hình logging cho ứng dụng
"""
import sys
from pathlib import Path
from loguru import logger

from src.config import LOG_LEVEL, LOG_PATH


def setup_logger():
    """
    Thiết lập cấu hình logger
    """
    # Tạo thư mục logs nếu chưa tồn tại
    log_path = Path(LOG_PATH)
    log_path.parent.mkdir(exist_ok=True)
    
    # Xóa cấu hình mặc định
    logger.remove()
    
    # Thêm cấu hình mới
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Thêm file log
    logger.add(
        LOG_PATH,
        level=LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="00:00",  # Tạo file log mới mỗi ngày
        retention="30 days"  # Giữ log trong 30 ngày
    )
    
    logger.info(f"Logger đã được thiết lập với mức {LOG_LEVEL}")
    logger.info(f"Log file: {LOG_PATH}")
    
    return logger
