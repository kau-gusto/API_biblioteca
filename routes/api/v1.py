from flask import request, session

from app import app
from utils.middlewares import require_authentication, require_admin, api
from utils.utils import allowed_file, set_uploaded_file, validate_form
from models import User, Book
from repositories.library import Repository as LibraryRepository
from repositories.users import Repository as UserRepository


@app.post("/api/v1/login")
@api
def login():
    session.clear()
    form = validate_form(dict(request.form))
    if form is None:
        return "Not Acceptable", 406

    if('email' not in form) or ('password' not in form):
        return "Unauthorized", 401

    usuario = UserRepository.get_user_by_email(form['email'])
    if(usuario is None):
        return "Unauthorized", 401

    if(form['password'] != usuario.password):
        return "Unauthorized", 401

    session["user"] = usuario.to_dict()
    return "Ok", 200


@app.get("/api/v1/logout")
@api
@require_authentication
def deslogar():
    session.clear()
    return "Ok", 200


@app.post("/api/v1/user/register")
@api
@require_admin
def register_user():
    form = validate_form(dict(request.form))
    if form is None:
        return "Not Acceptable", 406

    if "email" not in form:
        return "Not Acceptable", 406

    user = UserRepository.get_user_by_email(form['email'])
    if not user is None:
        return "Conflict", 409

    if "is_admin" not in form:
        return "Not Acceptable", 406

    is_admin = form['is_admin']
    form['is_admin'] = True if is_admin == "True"\
        else False if is_admin == "False"\
        else None
    if is_admin is None:
        return "Not Acceptable", 406

    id = UserRepository.get_last_id()+1
    try:
        form['id'] = id
        user = User(**form)
    except:
        return "Not Acceptable", 406

    UserRepository.set_new_user(user)

    return "Ok", 200


@app.get("/api/v1/users")
@api
@require_admin
def get_users():
    usuarios = UserRepository.get_users()
    send_users = []
    for _, usuario in usuarios.items():
        del usuario.password
        send_users.append(usuario.to_dict())
    return send_users, 200


@app.get("/api/v1/user/<id>")
@api
@require_admin
def get_user(id):
    user = UserRepository.get_user_by_id(id)
    if user is None:
        return "Not Found", 404
    return user.to_dict()


@app.get("/api/v1/info")
@api
@require_admin
def get_info():
    id = session["user"]["id"]
    user = UserRepository.get_user_by_id(id)
    if user is None:
        return "Server no reply", 500
    return user.to_dict()


@app.get("/api/v1/books")
@api
@require_authentication
def get_books():
    books = LibraryRepository.get_books()
    send_books = []
    for _, book in books.items():
        send_books.append(book.to_dict())
    return send_books, 200


@app.post("/api/v1/book/edit/<isbn10>")
@api
@require_admin
def edit_book(isbn10):
    form = validate_form(dict(request.form))
    if form is None:
        return "Not Acceptable", 406

    book = LibraryRepository.get_book_by_isbn10(isbn10)
    if book is None:
        return "Conflict", 409

    set_file = False
    for key, value in book.to_dict().items():
        if key == 'cover':
            if "cover" not in form:
                if 'file' in request.files:
                    file = request.files['file']
                    if not allowed_file(file.filename):
                        return "Not Acceptable", 406
                    set_file = True
                    ext = "." + file.filename.split(".")[-1].lower()
                    form['cover'] = app.config['UPLOAD_FOLDER'] + isbn10 + ext
        elif key not in form:
            form[key] = value

    try:
        new_book = Book(**form)
    except:
        return "Not Acceptable", 406

    if not LibraryRepository.update_book_by_isnb10(isbn10, new_book):
        return "Conflict", 409
    if set_file:
        set_uploaded_file(app.config['UPLOAD_FOLDER'], file, isbn10 + ext)

    return "Ok", 200


@app.post("/api/v1/book/register")
@api
@require_admin
def register_book():
    form = validate_form(dict(request.form))
    if form is None:
        return "Not Acceptable", 406

    if "isbn10" not in form:
        return "Not Acceptable", 406

    isbn10 = form["isbn10"]
    book = LibraryRepository.get_book_by_isbn10(isbn10)

    if not book is None:
        return "Conflict", 409

    set_file = False
    if "obs" not in form:
        form['obs'] = ''
    if "cover" not in form:
        if 'file' not in request.files:
            return "Not Acceptable", 406
        set_file = True
        file = request.files['file']
        if not allowed_file(file.filename):
            return "Not Acceptable", 406
        ext = "." + file.filename.split(".")[-1].lower()
        form['cover'] = app.config['UPLOAD_FOLDER'] + isbn10 + ext

    try:
        new_book = Book(**form)
    except:
        return "Not Acceptable", 406

    if not LibraryRepository.set_book(new_book):
        return "Conflict", 409
    if set_file:
        set_uploaded_file(app.config['UPLOAD_FOLDER'], file, isbn10 + ext)
    return "Ok", 200


@app.post("/api/v1/book/lending")
@api
@require_authentication
def lending_book():
    form = validate_form(dict(request.form))
    if form is None:
        return "Not Acceptable", 406
    if 'isbn10' not in form:
        return "Not Acceptable", 406
    isbn10 = form['isbn10']
    book = LibraryRepository.get_book_by_isbn10(isbn10)
    if book is None:
        return "Not Found", 404
    if book.on_loan:
        return "Conflict", 409

    book.on_loan = True
    LibraryRepository.update_book_by_isnb10(isbn10, book)
    user = UserRepository.get_user_by_id(session["user"]['id'])
    if user is None:
        return "Conflict", 409
    user.books_ids.append(isbn10)
    UserRepository.update_user_by_id(user.id, user)

    session["user"] = user.to_dict()

    return "Ok", 200


@app.get("/api/v1/book/<isbn10>")
@api
@require_authentication
def get_book(isbn10):
    book = LibraryRepository.get_book_by_isbn10(isbn10)
    if book is None:
        return "Not Found", 404
    return book.to_dict()
