from models.user import User, Users
from utils.database import get_json, set_json, create_json


usuarios = {
    1: {"id": 1,
        "email": "user@email.com",
        "name": "usuario",
        "password": "1234",
        "is_admin": False,
        "books_ids": [],
        },
    2: {"id": 2,
        "email": "admin@email.com",
        "name": "administrador",
        "password": "4321",
        "is_admin": True,
        "books_ids": [],
        }
}
create_json("users", usuarios)


class Repository:
    @classmethod
    def get_users(cls):
        return Users.get_users(get_json("users"))

    @classmethod
    def get_user_by_email(cls, email: str) -> User or None:
        users = Users.get_users(get_json("users"))
        for _, user in users.items():
            if user.email == email:
                return user
        return None

    @classmethod
    def get_user_by_id(cls, id: int) -> User or None:
        users = get_json("users")
        id = str(id)
        if id in users:
            return User(**users[id])
        return None

    @classmethod
    def update_user_by_id(cls, id: int, user: User):
        users = Users.get_users(get_json("users"))
        if id in users:
            users[id] = user
            set_json('users', Users.get_dict_users(users))
            return True
        return False

    @classmethod
    def set_new_user(cls, user: User):
        users = Users.get_users(get_json("users"))
        users[cls.get_last_id()+1] = user
        set_json("users", Users.get_dict_users(users))

    @classmethod
    def get_last_id(cls):
        users = Users.get_users(get_json("users"))
        list_id = list(users)
        return int(list_id[-1])
