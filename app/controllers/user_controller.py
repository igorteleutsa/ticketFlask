from app.models.user import User
from app.models.group import Group
from app.models.role import Role
from app import db
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


def get_all_users() -> list[User]:
    return User.query.all()


def create_user(username: str, email: str, password: str, role_id: str, group_ids: Optional[list[str]] = None) -> User:
    user = User(username=username, email=email, password=password, role_id=role_id)
    if group_ids:
        groups = Group.query.filter(Group.id.in_(group_ids)).all()
        user.groups.extend(groups)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(user_id: str) -> User:
    return User.query.get(user_id)


def update_user(user_id: str, username: str, email: str, role_id: str, group_ids: Optional[list[str]] = None) -> User:
    user = get_user_by_id(user_id)
    user.username = username
    user.email = email
    user.role_id = role_id
    if group_ids:
        groups = Group.query.filter(Group.id.in_(group_ids)).all()
        user.groups = groups
    db.session.commit()
    return user


def delete_user(user_id: str) -> None:
    user = get_user_by_id(user_id)
    db.session.delete(user)
    db.session.commit()


def get_all_roles() -> list[Role]:
    return Role.query.all()


def get_all_groups() -> list[Group]:
    return Group.query.all()


def check_email_exists(email: str) -> bool:
    return User.query.filter_by(email=email).first() is not None


def register_user(username: str, email: str, password: str, role_id: str, group_ids: Optional[list[str]] = None) -> Optional[User]:
    if check_email_exists(email):
        return None
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    return create_user(username, email, hashed_password, role_id, group_ids)


def authenticate_user(email: str, password: str) -> Optional[User]:
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None
