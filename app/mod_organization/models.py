
from app import db

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

# Define the  model
class App(Base):
    __tablename__ = 'apps'

    name = db.Column(db.String(30), nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name):
        self.name = name
        self.archive = False

    def __repr__(self):
        return '<App %r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "name": self.name,
            "archive": self.archive
        }

# Define the  model
class Organization(Base):
    __tablename__ = 'organizations'

    name = db.Column(db.String(30), nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name):
        self.name = name
        self.archive = False

    def __repr__(self):
        return '<Organization %r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "name": self.name,
            "archive": self.archive
        }

class Group(Base):
    __tablename__ = 'groups'

    organizationId = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(30), nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, organizationId, name):
        self.organizationId = organizationId
        self.name = name
        self.archive = False

    def __repr__(self):
        return '<Group %r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "organizationId": self.organizationId,
            "name": self.name,
            "archive": self.archive
        }
