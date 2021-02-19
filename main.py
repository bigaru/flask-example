from flask import Flask, request, jsonify, abort, make_response
from marshmallow import Schema, fields, ValidationError
from sqlalchemy import exc
from controller import BookController
from model import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:postgres@localhost/demo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    base = '/api/v1'

    controller = BookController(db)

    app.route(base + '/books/')(controller.get_all)
    app.route(base + '/books/<isbn>')(controller.get)
    app.route(base + '/books/', methods=["POST"])(controller.create)
    app.route(base + '/books/<isbn>', methods=["PUT"])(controller.update)
    app.route(base + '/books/<isbn>', methods=['DELETE'])(controller.delete)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)