#!/usr/bin/env python3
"""
Test script cho Chatbot Tư vấn Tâm lý Quân nhân
Kiểm tra các component chính của hệ thống
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.data_processor import DataProcessor
from src.embedding_system import EmbeddingSystem
from src.llm_system import LLMSystem
from src.chatbot_workflow import ChatbotWorkflow
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_data_processor():
    """Test data processor"""
    print("🧪 Testing Data Processor...")
    try:
        processor = DataProcessor(Config.DATA_FILE)
        data = processor.load_data()
        qa_pairs = processor.get_qa_pairs()
        documents = processor.get_documents_for_embedding()
        
        print(f"✅ Loaded {len(data)} records")
        print(f"✅ Generated {len(qa_pairs)} QA pairs")
        print(f"✅ Created {len(documents)} documents for embedding")
        
        return True
    except Exception as e:
        print(f"❌ Data processor test failed: {e}")
        return False

def test_embedding_system():
    """Test embedding system"""
    print("\n🧪 Testing Embedding System...")
    try:
        embedding_system = EmbeddingSystem()
        
        # Test embedding generation
        test_texts = ["Tôi cảm thấy căng thẳng", "Tôi nhớ nhà"]
        embeddings = embedding_system.get_embeddings(test_texts)
        
        print(f"✅ Generated embeddings for {len(test_texts)} texts")
        print(f"✅ Embedding dimension: {len(embeddings[0])}")
        
        # Test collection info
        info = embedding_system.get_collection_info()
        print(f"✅ Collection info: {info}")
        
        return True
    except Exception as e:
        print(f"❌ Embedding system test failed: {e}")
        return False

def test_llm_system():
    """Test LLM system"""
    print("\n🧪 Testing LLM System...")
    try:
        if not Config.GOOGLE_API_KEY:
            print("⚠️  Skipping LLM test - No API key provided")
            return True
        
        llm_system = LLMSystem()
        
        # Test response generation
        test_question = "Tôi cảm thấy căng thẳng sau buổi huấn luyện"
        response = llm_system.generate_response(test_question)
        
        print(f"✅ Generated response: {len(response)} characters")
        
        # Test sentiment analysis
        sentiment = llm_system.analyze_sentiment(test_question)
        print(f"✅ Sentiment analysis: {sentiment}")
        
        return True
    except Exception as e:
        print(f"❌ LLM system test failed: {e}")
        return False

def test_workflow():
    """Test chatbot workflow"""
    print("\n🧪 Testing Chatbot Workflow...")
    try:
        if not Config.GOOGLE_API_KEY:
            print("⚠️  Skipping workflow test - No API key provided")
            return True
        
        workflow = ChatbotWorkflow()
        
        # Test message processing
        test_question = "Tôi cảm thấy căng thẳng và lo lắng"
        result = workflow.process_message(test_question)
        
        print(f"✅ Workflow processed message")
        print(f"✅ Response length: {len(result['response'])} characters")
        print(f"✅ Sentiment: {result['sentiment']}")
        print(f"✅ Follow-up questions: {len(result['follow_up_questions'])}")
        
        return True
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

def test_database_initialization():
    """Test database initialization"""
    print("\n🧪 Testing Database Initialization...")
    try:
        workflow = ChatbotWorkflow()
        workflow.initialize_database()
        
        # Check collection info
        info = workflow.embedding_system.get_collection_info()
        print(f"✅ Database initialized with {info['document_count']} documents")
        
        return True
    except Exception as e:
        print(f"❌ Database initialization test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🎖️  Chatbot Tư vấn Tâm lý Quân nhân - System Test")
    print("=" * 60)
    
    tests = [
        ("Data Processor", test_data_processor),
        ("Embedding System", test_embedding_system),
        ("LLM System", test_llm_system),
        ("Chatbot Workflow", test_workflow),
        ("Database Initialization", test_database_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
