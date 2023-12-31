import os

# Created On 28-11-2022 at 15:21

# Debug Mode 
DEBUG = os.environ['DEBUG']
SECRET_KEY = os.environ["SECRET_KEY"]
SERVER = os.environ["SERVER"]

# Admin os.environ.geturation
ADMIN_SITE_HEADER = os.environ["ADMIN_SITE_HEADER"]

# Production Databse
RDS_PRODUCTION_DB_NAME = os.environ["RDS_PRODUCTION_DB_NAME"]
RDS_PRODUCTION_DB_USERNAME = os.environ["RDS_PRODUCTION_DB_USERNAME"]
RDS_PRODUCTION_DB_PASSWORD = os.environ["RDS_PRODUCTION_DB_PASSWORD"]
RDS_PRODUCTION_DB_HOSTNAME = os.environ["RDS_PRODUCTION_DB_HOSTNAME"]
RDS_PRODUCTION_DB_PORT = os.environ["RDS_PRODUCTION_DB_PORT"]

# AWS S3 Connection
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"] 
S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]
REGION_NAME = os.environ["REGION_NAME"]
MEDIA_BUCKET= os.environ["MEDIA_BUCKET"]

# Email os.environ.getuaration 
EMAIL_HOST_USER_NAME  = os.environ["EMAIL_HOST_USER_NAME"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

PAYMENT_TEST_API_KEY = os.environ["PAYMENT_TEST_API_KEY"]
PAYMENT_TEST_SECRET_KEY = os.environ["PAYMENT_TEST_SECRET_KEY"]

