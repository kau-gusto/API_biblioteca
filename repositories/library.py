from models.book import Books, Book
from utils.database import get_json, set_json, create_json

books = {
    "abcd1234": {
        'isbn10': "abcd1234",
        'title': "abcd",
        'sub_title': "1234",
        'author': "this",
        'edition': "2021",
        'year': "2020",
    },
    "1234abcd": {
        'isbn10': "1234abcd",
        'title': "1234",
        'sub_title': "abcd",
        'author': "this",
        'edition': "2021",
        'year': "2020",
    }
}

create_json("library", books)


class Repository:

    @classmethod
    def get_books(cls):
        return Books.get_books(get_json('library'))

    @classmethod
    def get_book_by_isbn10(cls, isbn10: str) -> None or Book:
        books = Books.get_books(get_json('library'))
        if isbn10 not in books:
            return None
        return books[isbn10]

    @classmethod
    def set_book(cls, book: Book):
        books = Books.get_books(get_json('library'))
        books[book.isbn10] = book
        set_json("library", Books.get_dict_books(books))
        return True

    @classmethod
    def update_book_by_isnb10(cls, isbn10: int, book: Book):
        books = Books.get_books(get_json('library'))
        if isbn10 not in books:
            return False
        books[isbn10] = book
        set_json("library", Books.get_dict_books(books))
        return True
