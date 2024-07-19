from app.models.group import Group
from app import db


def get_all_groups() -> list[Group]:
    return Group.query.all()


def create_group(name: str) -> Group:
    group = Group(name=name)
    db.session.add(group)
    db.session.commit()
    return group


def get_group_by_id(group_id: str) -> Group:
    return Group.query.get(group_id)
