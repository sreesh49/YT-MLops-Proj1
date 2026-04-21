import boto3
import tempfile
import os

# Create a test file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write("Test upload")
    test_file = f.name

# Try uploading to the correct bucket
s3 = boto3.client('s3')
bucket_name = "my-model-mlopsproj-12345"  # Your actual bucket name
test_key = "test_upload.txt"

try:
    s3.upload_file(test_file, bucket_name, test_key)
    print(f"✅ Success! Uploaded to s3://{bucket_name}/{test_key}")
    
    # Clean up
    s3.delete_object(Bucket=bucket_name, Key=test_key)
    print("✅ Test file cleaned up")
except Exception as e:
    print(f"❌ Failed: {e}")
finally:
    os.unlink(test_file)