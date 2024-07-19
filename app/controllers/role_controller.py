from app.models.role import Role
from app.models.permission import Permission
from app import db


def create_role(name: str, permissions: list[str]) -> Role:
    role = Role(name=name)
    for permission_name in permissions:
        permission = Permission.query.filter_by(name=permission_name).first()
        if permission:
            role.permissions.append(permission)
    db.session.add(role)
    db.session.commit()
    return role


def get_role_by_name(name: str) -> Role:
    return Role.query.filter_by(name=name).first()


def add_permission_to_role(role_name: str, permission_name: str) -> Role:
    role = get_role_by_name(role_name)
    permission = Permission.query.filter_by(name=permission_name).first()
    if role and permission:
        role.permissions.append(permission)
        db.session.commit()
    return role
