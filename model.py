from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()


class BookModel(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float())

    def __init__(self, isbn, name, price):
        self.isbn = isbn
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Book {self.isbn} {self.name} {self.price}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, isbn, name, price):
        self.isbn = isbn
        self.name = name
        self.price = price

class BookSchema(Schema):
    isbn = fields.String(required=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)