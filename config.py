import os

file_extentions = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
url_characters = "abcdefghjkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
upload_directory = "images"
default_url_length = 8
app_path = os.environ.get('APP_URL', '127.0.0.1:5000')
app_password = os.environ.get('APP_PASS', 'password')
app_username = os.environ.get('APP_USER', 'admin')

aws_access_key = os.environ.get('AWS_ACCESS_KEY')
aws_secret_key = os.environ.get('AWS_SECRET_KEY')

aws_s3_endpoint = 's3.amazonaws.com'
aws_s3_bucket_id = 'varney-me-images'
aws_s3_bucket_path = 'images'

db_url = os.environ.get("DB_URL")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASS")