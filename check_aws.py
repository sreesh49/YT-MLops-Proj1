import boto3
import os

print("=== AWS CREDENTIALS CHECK ===")

# Check environment variables
print("\n1. Environment Variables:")
print(f"AWS_ACCESS_KEY_ID: {'SET' if os.getenv('AWS_ACCESS_KEY_ID') else 'NOT SET'}")
print(f"AWS_SECRET_ACCESS_KEY: {'SET' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'NOT SET'}")
print(f"AWS_DEFAULT_REGION: {os.getenv('AWS_DEFAULT_REGION', 'NOT SET')}")

# Check if boto3 can find credentials
print("\n2. Boto3 Credentials Check:")
try:
    session = boto3.Session()
    credentials = session.get_credentials()
    if credentials:
        print(f"Credentials found! Access Key: {credentials.access_key[:10]}...")
        print(f"Region: {session.region_name or 'NOT SET'}")
    else:
        print("No credentials found!")
except Exception as e:
    print(f"Error: {e}")

# Try to list S3 buckets
print("\n3. Testing S3 Access:")
try:
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    print(f"Success! Found {len(response['Buckets'])} buckets:")
    for bucket in response['Buckets']:
        print(f"  - {bucket['Name']}")
except Exception as e:
    print(f"Failed: {e}")