from models.book import Books, Book
from utils.database import database

books = database.books


class Repository:

    @classmethod
    def get_books(cls):
        return Books.get_books(books.find())

    @classmethod
    def get_book_by_isbn10(cls, isbn10: str) -> None or Book:
        return Books.get_books(books.find_one({"isbn10": isbn10}))

    @classmethod
    def set_book(cls, book: Book):
        if not books.find_one({"isbn10": book.isbn10}) is None:
            return False
        books.insert_one(Books.get_dict_books(book))
        return True

    @classmethod
    def update_book_by_isnb10(cls, isbn10: int, book: Book):
        if books.find_one({"isbn10": isbn10}) is None:
            return False
        books.update_one({"isbn10": isbn10}, Books.get_dict_books(book))
        return True
