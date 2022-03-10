from flask import Flask

UPLOAD_FOLDER = 'public/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask('Api Biblioteca',
            static_url_path='', static_folder="public")
