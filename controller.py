from model import BookSchema, BookModel
from flask import request, jsonify, abort, make_response
from sqlalchemy import exc
from marshmallow import ValidationError


class BookController:
    def __init__(self, db):
        self.db = db
        self.bookSchema = BookSchema()

    def __validate_format(self, payload):
        try:
            self.bookSchema.load(payload)
        except ValidationError as err:
            abort(make_response(jsonify(err.messages), 400))        

    def get_all(self):
        data = BookModel.query.all()
        data = list(map(lambda x: x.as_dict(), data))
        return jsonify(data), 200
    
    def get(self, isbn):
        maybeBook = BookModel.query.get(isbn)

        if maybeBook is None:
            return jsonify(message="item not found"), 404

        return maybeBook.as_dict(), 200

    def create(self):
        payload = request.json
        self.__validate_format(payload)
            
        try:
            newBook = BookModel(**payload)
            self.db.session.add(newBook)
            self.db.session.commit()
            return jsonify(payload), 201

        except exc.IntegrityError:
            return jsonify(message="isbn exists already"), 400

    def update(self, isbn):
        payload = request.json
        self.__validate_format(payload)
        isbn_payload = payload['isbn']

        if isbn != isbn_payload:
            return jsonify(message="isbn did not match"), 400

        maybeBook = BookModel.query.get(isbn)

        if maybeBook is None:
            newBook = BookModel(**payload)
            self.db.session.add(newBook)

        else:
            maybeBook.update(**payload)
            
        self.db.session.commit()
        return jsonify(payload), 200
    
    def delete(self, isbn):
        maybeBook = BookModel.query.get(isbn)

        if maybeBook is not None:
            self.db.session.delete(maybeBook)
            self.db.session.commit()
            return jsonify(message="deleted successfully"), 200

        return jsonify(message="item not found"), 404