from flask import Flask, request, send_from_directory, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename
from functools import wraps
import tinys3
import random, os, config

#Setup
application = Flask(__name__)
#aws_client = boto3.client(service_name = 's3', aws_access_key_id=config.aws_access_key, aws_secret_access_key=config.aws_secret_key)
print(config.aws_access_key, config.aws_secret_key)
s3_connection = tinys3.Connection(config.aws_access_key, config.aws_secret_key, tls=True, endpoint=config.aws_s3_endpoint)


#Load Configuration Variables
application.config['ALLOWED_EXTENSIONS'] = config.file_extentions
application.config['UPLOAD_DIRECTORY'] = config.upload_directory
application.config['URL_LENGTH'] = config.default_url_length
application.config['ALPHA_CHARS'] = config.url_characters
application.config['PATH'] = config.app_path
application.config['USER'] = config.app_username
application.config['PASSWORD'] = config.app_password

#Create the temporary directory to save images
if not os.path.exists(application.config['UPLOAD_DIRECTORY']):
    os.mkdir(application.config['UPLOAD_DIRECTORY'])


#App Methods

def strip_extenstion(filename: str) -> str:
    '''
    Strips the file extension from a file
    :param filename: A filename, such as 'example.txt'
    :return: A string of the extension type, such as 'txt', or None if there is no extension
    '''
    if '.' in filename:
        return filename.lower().rsplit('.', 1)[1]

    return None

def is_acceptable_filename(filename: str) -> bool:
    '''
    is_acceptable_file() helps check whether or not a file satisfied the requirement of being an image

    :param filename: Name of the file
    :return: A boolean indicating whether or not a file satisfies the requirements for an image
    '''

    return strip_extenstion(filename) in application.config['ALLOWED_EXTENSIONS']

def generate_random_string(length = application.config['URL_LENGTH']) -> str:
    '''
    :param length: Length of string to generate
    :return: A string of random digits from the ALPHA_CHARS config
    '''

    return ''.join([random.choice(application.config['ALPHA_CHARS']) for x in range(length)])

def check_auth(username, password):
    return username == application.config['USER'] and password == application.config['PASSWORD']

def get_images():
    return os.listdir(application.config['UPLOAD_DIRECTORY'])


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def make_s3_upload(bucket_name:str, destination_directory, key_name, path_to_file):

    with open(path_to_file, 'rb') as file:

        s3_path = os.path.join(destination_directory, key_name)

        s3_connection.upload(s3_path, file, bucket_name)



#Decorators

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#App Routes
@application.route('/')
def hello_world():
    return "ImageServer running on " + application.config['PATH']

@application.route('/<filename>/', methods=['GET'])
def get_image(filename = None):
    if filename:
        aws_url = 'http://' + config.aws_s3_endpoint + '/' + config.aws_s3_bucket_id + '/' + config.aws_s3_bucket_path + '/' + filename
        return render_template('display_image.html', app_path = config.app_path, image_url=aws_url)
    else:
        return '404'

@application.route('/upload/', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        file = request.files['file']
        if file and is_acceptable_filename(file.filename):
            new_filename = '{0}.{1}'.format(generate_random_string(), strip_extenstion(file.filename))
            local_temp_path = os.path.join(application.config['UPLOAD_DIRECTORY'], new_filename)


            file.save(local_temp_path)
            make_s3_upload(config.aws_s3_bucket_id, config.aws_s3_bucket_path, new_filename, local_temp_path)
            os.remove(local_temp_path)

            return '{}/{}'.format(config.app_path, new_filename)

        else:
            return "An invalid operation was attempted."
    else:
        return render_template('upload_form.html')


@application.route('/<filename>/delete/')
@requires_auth
def delete_img(filename = None):
    if filename:
        sanitized_filename = secure_filename(filename)
        if os.path.exists(os.path.join(application.config['UPLOAD_DIRECTORY'], sanitized_filename)):
            os.remove(os.path.join(application.config['UPLOAD_DIRECTORY'], sanitized_filename))
            return "The file has been deleted."
        else:
            return "The file does not exist on this server."

@application.route('/list/')
def list_files():
    return render_template('list_images.html', file_list = get_images(), base_url = application.config['PATH'])

if __name__ == '__main__':
    application.run('0.0.0.0', debug=True)
