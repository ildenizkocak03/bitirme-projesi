# Configuration settings for Customer Review AI Platform

# Model configurations
SENTIMENT_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
TOPIC_MODEL = "all-MiniLM-L6-v2"

# Risk assessment thresholds
RISK_THRESHOLDS = {
    'low': 0.3,
    'medium': 0.5,
    'high': 0.8,
    'critical': 0.8  # Same as high but with different labeling logic
}

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000

# Streamlit settings
STREAMLIT_PORT = 8501

# File upload settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = ['csv']

# Analysis settings
BATCH_SIZE = 32
MAX_TEXT_LENGTH = 512