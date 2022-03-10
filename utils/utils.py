import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def validate_string(text: str):
    text = text.strip()
    if text != "":
        return text
    return None


def validate_form(form: dict):
    new_form = {}
    for index, value in form.items():
        new_form[index] = validate_string(value)
        if new_form[index] is None:
            return None
    return new_form


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def set_uploaded_file(path: str, file: FileStorage, filename: str):
    if file.filename == '':
        return "Not Acceptable", 406
    if not file and not allowed_file(filename):
        return "Not Acceptable", 406
    filename = secure_filename(filename)
    file.save(os.path.join(path, filename))
    return "Ok", 200
