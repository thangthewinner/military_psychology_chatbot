# Chatbot Tư Vấn Tâm Lý Quân Nhân

Hệ thống chatbot tư vấn tâm lý cho quân nhân trong quân đội dựa trên kỹ thuật RAG (Retrieval Augmented Generation).

## Tính năng

- Tư vấn tâm lý cho quân nhân dựa trên cơ sở dữ liệu tâm lý quân sự
- Sử dụng kỹ thuật RAG để tìm kiếm và tạo câu trả lời chính xác
- Giao diện người dùng thân thiện với Streamlit
- Hệ thống logging đầy đủ

## Cấu trúc dự án

```
nguyenvietong_chatbot/
├── data/                  # Thư mục chứa dữ liệu
│   └── military_psychology.csv
├── logs/                  # Thư mục chứa log
├── src/                   # Mã nguồn
│   ├── __init__.py
│   ├── config.py          # Cấu hình
│   ├── logger.py          # Hệ thống logging
│   ├── data_processor.py  # Xử lý dữ liệu
│   ├── embedding_system.py # Hệ thống embedding
│   ├── llm_system.py      # Tương tác với LLM
│   ├── rag_system.py      # Hệ thống RAG
│   ├── chatbot.py         # Chatbot
│   ├── database_setup.py  # Thiết lập vector database
│   └── streamlit_app.py   # Ứng dụng Streamlit
├── vector_db/            # Vector database (tạo tự động)
├── .env                  # Biến môi trường (cần tạo từ .env.example)
├── .env.example          # Mẫu biến môi trường
├── main.py               # File chạy chính
└── requirements.txt      # Các thư viện cần thiết
```

## Cài đặt

1. Clone repository:

```bash
git clone <repository-url>
cd nguyenvietong_chatbot
```

2. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

3. Tạo file `.env` từ mẫu `.env.example`:

```bash
cp .env.example .env
```

4. Cập nhật file `.env` với API key của Groq:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Sử dụng

### 1. Khởi tạo vector database

Trước khi sử dụng chatbot, cần khởi tạo vector database:

```bash
python main.py --setup-db
```

### 2. Khởi động ứng dụng

```bash
python main.py --run-app
```

Sau khi chạy lệnh trên, ứng dụng Streamlit sẽ được khởi động và có thể truy cập qua trình duyệt web tại địa chỉ `http://localhost:8501`.

## Công nghệ sử dụng

- **Embedding Model**: Alibaba-NLP/gte-multilingual-base
- **Vector Database**: FAISS
- **LLM**: llama-3.3-70b-versatile (qua Groq API)
- **Giao diện**: Streamlit
- **Các công nghệ khác**: LangChain, LangGraph, Loguru

## Lưu ý

- Đảm bảo đã cài đặt đầy đủ các thư viện trong `requirements.txt`
- Cần có API key của Groq để sử dụng mô hình LLM
- Vector database cần được khởi tạo trước khi sử dụng chatbot
