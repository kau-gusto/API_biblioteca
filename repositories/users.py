from models.user import User, Users
from utils.database import database

usuarios = database.usuarios


class Repository:
    @classmethod
    def get_users(cls):
        return Users.get_users(usuarios.find())

    @classmethod
    def get_user_by_email(cls, email: str) -> User or None:
        return User(**usuarios.find_one({"email": email}))

    @classmethod
    def get_user_by_id(cls, id: int) -> User or None:
        return User(**usuarios.find_one({"_id": id}))

    @classmethod
    def update_user_by_id(cls, id: int, user: User) -> bool:
        localUser = usuarios.find_one({"_id": id})
        if not localUser is None:
            usuarios.update_one({'_id': id}, user.to_dict())
            return True
        return False

    @classmethod
    def set_new_user(cls, user: User) -> bool:
        if not usuarios.find_one({"_id", User.id}) is None:
            usuarios.insert_one("users", user.to_dict())
            return True
        return False
