from app import db
from app.models.base import BaseModel


class Permission(BaseModel):
    __tablename__ = 'permission'
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Permission {self.name}>'
