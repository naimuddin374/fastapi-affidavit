from s3_service import S3Service
from dotenv import load_dotenv  # Need 'pip install python-dotenv'
import os

load_dotenv()


# Example usage demonstrating the methods

# 1. Setup Environment Variables (MANDATORY for Boto3 to work)
# In a real FastAPI app, you would set these in your .env file or Docker Compose.
# os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_ACCESS_KEY'
# os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_SECRET_KEY'
# --- Initialization ---
AWS_BUCKET = os.environ.get(
    "AWS_BUCKET_NAME") | "my-fastapi-file-storage-bucket"
AWS_REGION = os.environ.get("AWS_REGION") | "us-east-1"

# Create an instance of the service
s3_service = S3Service(bucket_name=AWS_BUCKET, region_name=AWS_REGION)

# --- Define a Test File ---
KEY_PATH = "uploads/user_123/profile_picture.jpg"
MIME_TYPE = "image/jpeg"

# 1. Generate PUT URL (For client to upload)
put_url = s3_service.generate_put_url(
    file_key=KEY_PATH,
    file_type=MIME_TYPE,
    expiration=600  # Valid for 10 minutes
)
if put_url:
    print("\n[1] GENERATED PUT URL (Client uses this to UPLOAD):")
    print(put_url)
    print(
        f"\nYour React app needs to PUT the file to this URL with Content-Type: {MIME_TYPE}")
    # In FastAPI, you would return this URL to the client.

# 2. Check Existence (Will be False initially)
exists_before = s3_service.object_exists(file_key=KEY_PATH)
print(f"\n[2] Object existence check (before upload): {exists_before}")

# 3. Generate GET URL (For client to download or display)
get_url = s3_service.generate_get_url(file_key=KEY_PATH, expiration=3600)
if get_url:
    print("\n[3] GENERATED GET URL (Client uses this to DOWNLOAD):")
    print(get_url)
    # This URL can be used in an <img> tag in your React app.

# 4. Delete Object (Example only—run this after upload is confirmed)
# delete_success = s3_service.delete_object(file_key=KEY_PATH)
# print(f"\n[4] Object deletion success: {delete_success}")

# 5. Check Existence (Should be False after deletion)
# exists_after = s3_service.object_exists(file_key=KEY_PATH)
# print(f"[5] Object existence check (after deletion): {exists_after}")
