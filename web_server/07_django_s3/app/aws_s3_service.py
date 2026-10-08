import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from datetime import datetime

class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            region_name = settings.AWS_S3_REGION_NAME,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    # 파일을 S3에 업로드하고 파일 URL 전체경로 반환하는 함수
    def upload(self,file):
        save_dir = 'upload/'    # S3 버킷내 저장 폴더
        now = datetime.now()    
        date_prefix = now.strftime('%Y%m%d_%H%M%S_')
        new_file_name = f"{date_prefix}{file.name}"
        extra_args = {'ContentType' : file.content_type}

        try:
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                f"{save_dir}{new_file_name}",
                ExtraArgs = extra_args
            )
            return f"https://{self.bucket_name}.s3.amazonaws.com/{save_dir}{new_file_name}"
        except NoCredentialsError:
            print('AWS 인증정보가 없습니다!')