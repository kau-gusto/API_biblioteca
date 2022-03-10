class Book:
    def __init__(self, isbn10: str,
                 title: str, sub_title: str,
                 author: str, edition: str, year: str,
                 obs: str = '', cover: str = '', on_loan=False,
                 ) -> None:
        self.isbn10 = isbn10
        self.title = title
        self.sub_title = sub_title
        self.author = author
        self.edition = edition
        self.year = year
        self.obs = obs
        self.cover = cover
        self.on_loan = on_loan

    def to_dict(self) -> dict[str, str]:
        return self.__dict__


class Books:
    @classmethod
    def get_books(cls, baseBooks: dict[str, dict]) -> dict[str, Book]:
        books = {}
        for isbn10, book in baseBooks.items():
            books[isbn10] = Book(**book)
        return books

    @classmethod
    def get_dict_books(cls, books: dict[str, Book]):
        send_books = {}
        for id, book in books.items():
            send_books[id] = book.to_dict()
        return send_books
