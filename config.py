import os

file_extentions = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
url_characters = "abcdefghjkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
upload_directory = "images"
default_url_length = 8
app_path = 'http://' + os.environ.get('APP_URL', "127.0.0.1:5000")
