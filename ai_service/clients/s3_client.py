import boto3
from botocore.exceptions import ClientError

from ai_service.config import settings


class S3Client:
    def __init__(self, bucket_name: str):
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            endpoint_url=settings.S3_BUCKET_URL,
        )
        self.bucket_name = bucket_name

    def ensure_bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            try:
                self.client.create_bucket(Bucket=self.bucket_name)
            except Exception as e:  # noqa: BLE001
                print(f"Error creating bucket {self.bucket_name}: {e}")


    def download_file(self, s3_key: str, local_path: str) -> str:
        self.client.download_file(Bucket=self.bucket_name, Key=s3_key, Filename=local_path)
        return local_path

