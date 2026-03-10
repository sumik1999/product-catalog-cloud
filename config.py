import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database - Supports both local and Cloud SQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/product_catalogue'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google Cloud SQL Configuration
    CLOUD_SQL_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME', '')
    
    # Google Cloud Storage
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', '')
    GCS_PROJECT_ID = os.environ.get('GCS_PROJECT_ID', '')
    GCS_CREDENTIALS_FILE = os.environ.get('GCS_CREDENTIALS_FILE', '')
    GCS_PUBLIC_URL_BASE = os.environ.get('GCS_PUBLIC_URL_BASE', '')
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
