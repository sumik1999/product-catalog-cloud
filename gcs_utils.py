import os
import uuid
from datetime import datetime
from google.cloud import storage
from config import Config

def get_gcs_client():
    creds_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or Config.GCS_CREDENTIALS_FILE
    if creds_file:
        return storage.Client.from_service_account_json(creds_file)
    return storage.Client()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def upload_to_gcs(file, bucket_name):
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME not configured")
    
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
    blob_name = f"products/{uuid.uuid4()}.{ext}"
    
    blob = bucket.blob(blob_name)
    blob.upload_from_file(file, content_type=file.content_type)
    
    if Config.GCS_PUBLIC_URL_BASE:
        return f"{Config.GCS_PUBLIC_URL_BASE}/{blob_name}"
    
    return blob.public_url

def delete_from_gcs(image_url, bucket_name):
    if not image_url or not bucket_name:
        return
    
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob_name = image_url.replace(f"{Config.GCS_PUBLIC_URL_BASE}/", "")
        blob = bucket.blob(blob_name)
        blob.delete()
    except Exception:
        pass
