import os

file_extentions = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
url_characters = "abcdefghjkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
upload_directory = "images"
default_url_length = 8
app_path = os.environ.get('APP_URL', "127.0.0.1:5000")
app_password = os.environ.get('APP_PASS', "password")
app_username = os.environ.get('APP_USER', "admin")
aws_access_key = os.environ.get('AWS_ACCESS_KEY', "<key_here>")
aws_secret_key = os.environ.get('AWS_SECRET_KEY', "<key_here>")