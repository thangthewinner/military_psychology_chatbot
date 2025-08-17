# 🎖️ Chatbot Tư vấn Tâm lý Quân nhân

Một chatbot thông minh được xây dựng để hỗ trợ tư vấn tâm lý cho quân nhân trong quân đội, sử dụng AI và machine learning để cung cấp lời khuyên phù hợp và đồng cảm.

## 🌟 Tính năng chính

- **Tư vấn tâm lý thông minh**: Sử dụng LLM (Google Gemini) để tạo câu trả lời chất lượng
- **Phân tích cảm xúc**: Tự động phân tích mức độ nghiêm trọng và cảm xúc của câu hỏi
- **Tìm kiếm ngữ cảnh**: Sử dụng vector database để tìm thông tin liên quan
- **Giao diện thân thiện**: Streamlit UI với thiết kế đẹp và dễ sử dụng
- **Workflow thông minh**: LangGraph workflow để xử lý conversation flow
- **Xuất lịch sử chat**: Khả năng xuất và lưu trữ cuộc trò chuyện
- **Cảnh báo khẩn cấp**: Tự động phát hiện và cảnh báo tình huống nghiêm trọng

## 🛠️ Công nghệ sử dụng

- **Frontend**: Streamlit
- **LLM**: Google Gemini (via LangChain)
- **Embedding**: Alibaba-NLP/gte-multilingual-base
- **Vector Database**: ChromaDB
- **Workflow**: LangGraph
- **Language**: Python 3.8+

## 📋 Yêu cầu hệ thống

- Python 3.8 hoặc cao hơn
- Google API Key cho Gemini
- RAM: Tối thiểu 4GB (khuyến nghị 8GB+)
- Disk space: 2GB cho models và database

## 🚀 Cài đặt và chạy

### 1. Clone repository
```bash
git clone <repository-url>
cd nguyenvietong_chatbot
```

### 2. Tạo virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Tạo file .env
Tạo file `.env` trong thư mục gốc với nội dung:
```env
GOOGLE_API_KEY=your_google_api_key_here
EMBEDDING_MODEL=Alibaba-NLP/gte-multilingual-base
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### 5. Chạy ứng dụng
```bash
# Cách 1: Sử dụng main.py
python main.py

# Cách 2: Sử dụng streamlit trực tiếp
streamlit run app.py
```

Ứng dụng sẽ chạy tại: http://localhost:8501

## 📁 Cấu trúc dự án

```
nguyenvietong_chatbot/
├── app.py                 # Streamlit application
├── main.py               # Entry point
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── README.md            # Documentation
├── .env                 # Environment variables
├── data/
│   └── military_psychology.csv  # Training data
├── src/
│   ├── __init__.py
│   ├── data_processor.py        # Data processing
│   ├── embedding_system.py      # Embedding & vector DB
│   ├── llm_system.py           # LLM integration
│   └── chatbot_workflow.py     # LangGraph workflow
└── chroma_db/           # Vector database (auto-created)
```

## 🎯 Cách sử dụng

### 1. Khởi tạo hệ thống
- Mở ứng dụng trong trình duyệt
- Nhấn "🚀 Khởi tạo Chatbot" trong sidebar
- Đợi hệ thống khởi tạo database và models

### 2. Bắt đầu trò chuyện
- Nhập câu hỏi của bạn vào ô chat
- Nhấn "📤 Gửi" hoặc Enter
- Chatbot sẽ phân tích và đưa ra lời khuyên

### 3. Tính năng bổ sung
- **Phân tích cảm xúc**: Mở rộng phần "📊 Phân tích cảm xúc" để xem chi tiết
- **Câu hỏi gợi ý**: Nhấn vào các câu hỏi gợi ý để tiếp tục cuộc trò chuyện
- **Xuất lịch sử**: Tải về file JSON chứa toàn bộ cuộc trò chuyện

## 🔧 Cấu hình

### Thay đổi model
Trong file `config.py`:
```python
LLM_MODEL = "gemini-pro"  # Thay đổi model LLM
EMBEDDING_MODEL = "Alibaba-NLP/gte-multilingual-base"  # Thay đổi embedding model
```

### Điều chỉnh tham số
```python
MAX_TOKENS = 1000        # Số token tối đa cho response
TEMPERATURE = 0.7        # Độ sáng tạo của LLM
TOP_K_RESULTS = 3        # Số kết quả tìm kiếm
```

## 📊 Dữ liệu

Dự án sử dụng dataset gồm 20 cặp câu hỏi-trả lời về tư vấn tâm lý quân nhân, bao gồm các chủ đề:
- Căng thẳng và áp lực trong huấn luyện
- Nỗi nhớ nhà và cảm giác cô đơn
- Khó khăn hòa nhập với đồng đội
- Mất ngủ và lo lắng trước nhiệm vụ
- Và nhiều chủ đề khác...

## 🚨 Lưu ý quan trọng

1. **Bảo mật**: Không chia sẻ Google API Key của bạn
2. **Giới hạn**: Chatbot chỉ hỗ trợ tư vấn cơ bản, không thay thế chuyên gia
3. **Khẩn cấp**: Với vấn đề nghiêm trọng, vui lòng tìm đến chuyên gia tâm lý
4. **Dữ liệu**: Cuộc trò chuyện được lưu trữ cục bộ, không gửi lên server

## 🆘 Hỗ trợ khẩn cấp

Khi cần hỗ trợ ngay lập tức, vui lòng liên hệ:
- Cán bộ tâm lý trong đơn vị
- Bác sĩ quân y
- Cấp trên trực tiếp
- Đường dây nóng hỗ trợ tâm lý quân đội

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

Dự án này được phát triển cho mục đích giáo dục và nghiên cứu.

## 📞 Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng tạo issue trên GitHub.

---

**Lưu ý**: Đây là một dự án demo và không thay thế cho việc tư vấn chuyên môn. Với các vấn đề tâm lý nghiêm trọng, vui lòng tìm đến chuyên gia có chuyên môn.