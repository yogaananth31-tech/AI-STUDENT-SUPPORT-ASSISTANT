import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Config:
    """Application configuration management for the AI Student Support Assistant."""
    
    # Flask / Express / Server settings
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("NODE_ENV", "development") == "development"
    
    # OpenAI & LLM Configurations
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Vector Database Settings
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # RAG Parameters
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    RETRIEVAL_K = 2

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
