import boto3
from botocore.exceptions import NoCredentialsError

# AWS credentials and bucket name
AWS_ACCESS_KEY = 'access key'
AWS_SECRET_KEY = 'secret key'
BUCKET_NAME = 'picameradetection'

def upload_to_s3(file_path, bucket_name=BUCKET_NAME, object_name=None):
    """
    Uploads a file to an S3 bucket.
    
    :param file_path: File to upload
    :param bucket_name: S3 bucket name
    :param object_name: S3 object name. If not specified, file_path is used
    :return: True if file was uploaded, else False
    """
    # Use the file name as the object name if none is provided
    if object_name is None:
        object_name = file_path.split('/')[-1]

    # Initialize the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    try:
        # Upload the file to S3
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to S3 bucket {bucket_name} as {object_name}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
