import boto3
from botocore.exceptions import ClientError
from typing import Optional


class S3Service:
    """
    A service class to encapsulate basic AWS S3 operations using boto3, 
    focusing on generating pre-signed URLs for direct client interaction.
    """

    def __init__(self, bucket_name: str, region_name: str = ''):
        """
        Initializes the S3 client. 

        It is assumed that AWS credentials (AWS_ACCESS_KEY_ID and 
        AWS_SECRET_ACCESS_KEY) are set in the environment variables.
        """
        self.bucket_name = bucket_name
        self.region_name = region_name
        try:
            self.s3_client = boto3.client(
                's3',
                region_name=self.region_name
            )
        except Exception as e:
            print(f"Error initializing S3 client: {e}")
            self.s3_client = None

    def generate_put_url(self, file_key: str, file_type: str, expiration: int = 3600) -> Optional[str]:
        """
        Generates a pre-signed URL for a client to securely upload a file (PUT).

        :param file_key: S3 object key (path and filename) where the file will be stored.
        :param file_type: The MIME type of the file (e.g., 'image/jpeg', 'application/pdf').
        :param expiration: Time in seconds for the URL to remain valid.
        :return: The generated pre-signed URL, or None on error.
        """
        if not self.s3_client:
            return None

        try:
            # We must specify ContentType so the client must match it when uploading
            response = self.s3_client.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_key,
                    'ContentType': file_type
                },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            print(f"Error generating PUT URL for {file_key}: {e}")
            return None

    def generate_get_url(self, file_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Generates a pre-signed URL to securely download a private object (GET).

        :param file_key: S3 object key (path and filename).
        :param expiration: Time in seconds for the URL to remain valid.
        :return: The generated pre-signed URL, or None on error.
        """
        if not self.s3_client:
            return None

        try:
            response = self.s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            print(f"Error generating GET URL for {file_key}: {e}")
            return None

    def delete_object(self, file_key: str) -> bool:
        """
        Deletes an object from the S3 bucket.

        :param file_key: S3 object key (path and filename).
        :return: True if successful, False otherwise.
        """
        if not self.s3_client:
            return False

        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            return True
        except ClientError as e:
            print(f"Error deleting object {file_key}: {e}")
            return False

    def object_exists(self, file_key: str) -> bool:
        """
        Checks if an object exists in the S3 bucket using head_object.

        :param file_key: S3 object key (path and filename).
        :return: True if the object exists, False otherwise.
        """
        if not self.s3_client:
            return False

        try:
            # head_object retrieves metadata without returning the object itself
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except ClientError as e:
            # The most common failure is a 404 (Not Found)
            if e.response['Error']['Code'] == '404':
                return False
            # Handle other errors (permissions, etc.)
            print(f"Error checking existence of {file_key}: {e}")
            return False
