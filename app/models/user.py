from app.database import db
from flask_login import UserMixin
from app.models.base import BaseModel
from app.models.role import Role


class User(UserMixin, BaseModel):
    __tablename__ = 'user'
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role_id = db.Column(db.String(36), db.ForeignKey('role.id'), nullable=False,
                        default=lambda: Role.query.filter_by(name='Analyst').first().id)
    groups = db.relationship('Group', secondary='user_groups', back_populates='users', lazy='subquery')
    tickets = db.relationship('Ticket', back_populates='user', overlaps="ticket_user", lazy=True)

    def has_permission(self, permission_name: str) -> bool:
        for permission in self.role.permissions:
            if permission.name == permission_name:
                return True
        return False

    def has_role(self, role_name):
        return self.role.name == role_name

    def __repr__(self) -> str:
        return f'<User {self.username}>'
