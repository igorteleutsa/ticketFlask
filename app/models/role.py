from app.database import db

from app.models.base import BaseModel


role_permissions = db.Table('role_permissions',
                            db.Column('role_id', db.String(36), db.ForeignKey('role.id'), primary_key=True),
                            db.Column('permission_id', db.String(36), db.ForeignKey('permission.id'), primary_key=True)
                            )


class Role(BaseModel):
    __tablename__ = 'role'
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)
    permissions = db.relationship('Permission', secondary=role_permissions, lazy='subquery',
                                  backref=db.backref('roles', lazy=True))

    def __repr__(self) -> str:
        return f'<Role {self.name}>'
