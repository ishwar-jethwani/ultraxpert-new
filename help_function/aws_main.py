import boto3
from django.conf import settings
from botocore.client import Config
from datetime import datetime


class AWSServices:
    """File Upload Function"""
    def __init__(self):
        self.access_key = settings.AWS_ACCESS_KEY_ID
        self.secret_key =  settings.AWS_SECRET_ACCESS_KEY
        self.media_bucket = settings.MEDIA_BUCKET
        self.region = settings.REGION_NAME
        
    def file_upload(self,file,filename,folder_name):
        self.bucket_obj = boto3.resource(
            "s3", 
            aws_access_key_id = self.access_key, 
            aws_secret_access_key = self.secret_key,
            config = Config(signature_version='s3v4')  
        )
        today = datetime.now()
        day = today.strftime("%b/%d/%Y")
        file_path = "{}/{}/{}".format(folder_name,day,filename)
        self.bucket = self.bucket_obj.Bucket(self.media_bucket)
        self.bucket.put_object(key=file_path, Body=file)
        object_acl = self.bucket_obj.ObjectAcl(self.media_bucket, file_path)
        response = object_acl.put(ACL='public-read')
        url = "https://{}.s3.{}.amazonaws.com/{}/{}".format(str(self.media_bucket), str(self.region), str(folder_name), str(day), str(filename))
        return url

    





