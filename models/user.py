class User:
    def __init__(self, id: int, name: str, email: str, password: str, is_admin: bool = False, books_ids: list = []) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.books_ids = books_ids

    def to_dict(self) -> dict[str, str]:
        return self.__dict__

    def __repr__(self) -> str:
        return f"User({self.name})#{self.id}"


class Users:
    @classmethod
    def get_users(cls, baseUsers: dict[str, dict]) -> dict[str, User]:
        users = {}
        for id, user in baseUsers.items():
            users[id] = User(**user)
        return users

    @classmethod
    def get_dict_users(cls, users: dict[str, User]):
        send_users = {}
        for id, user in users.items():
            send_users[id] = user.to_dict()
        return send_users
