from flask import Flask, request, send_from_directory, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import random, os, config

#Config Values:
ALLOWED_FILE_EXTENSTIONS = config.file_extentions
ALPHA_CHARS = config.url_characters
UPLOAD_DIRECTORY = config.upload_directory
DEFAULT_URL_LENGTH = config.default_url_length
APP_PATH = config.app_path

#Setup
application = Flask(__name__)
application.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY
application.config['PATH'] = APP_PATH

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

    return strip_extenstion(filename) in ALLOWED_FILE_EXTENSTIONS



def generate_random_string(length = DEFAULT_URL_LENGTH) -> str:
    '''
    :param length: Length of string to generate
    :return: A string of random digits from the ALPHA_CHARS config
    '''

    return ''.join([random.choice(ALPHA_CHARS) for x in range(length)])

#App Routes
@application.route('/')
def hello_world():
    return "ImageServer running on " + application.config['PATH']

@application.route('/<filename>/', methods=['GET'])
def get_image(filename = None):
    if filename and os.path.exists(os.path.join(application.config['UPLOAD_DIRECTORY'], filename)):
        return send_from_directory(application.config['UPLOAD_DIRECTORY'], filename)
    else:
        return '404'

@application.route('/upload/', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        file = request.files['file']
        if file and is_acceptable_filename(file.filename):
            new_filename = '{0}.{1}'.format(generate_random_string(), strip_extenstion(file.filename))
            file.save(os.path.join(application.config['UPLOAD_DIRECTORY'], new_filename))

            return application.config['PATH'] + url_for('get_image', filename=new_filename)

        else:
            return "An invalid operation was attempted."
    else:
        return render_template('upload_form.html')


@application.route('/<filename>/delete/')
def delete_img(filename = None):
    if filename:
        sanitized_filename = secure_filename(filename)
        if os.path.exists(os.path.join(application.config['UPLOAD_DIRECTORY'], sanitized_filename)):
            os.remove(os.path.join(application.config['UPLOAD_DIRECTORY'], sanitized_filename))
            return "The file has been deleted."
        else:
            return "The file does not exist on this server."

if __name__ == '__main__':
    application.run()
