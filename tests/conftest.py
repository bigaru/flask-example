import pytest
from flask_sqlalchemy import SQLAlchemy
from main import create_app
from model import BookModel, db

@pytest.fixture()
def app():
    app = create_app()
    app.debug = True

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def client(app):
    BookModel.query.delete()

    data = [
        { "isbn":"978-3840024634", "name": "Foo Master", "price": 9.99 },
        { "isbn":"878-3840024634", "name": "Bar", "price": 9.99 },
        { "isbn":"778-3840024634", "name": "Planer", "price": 9.99 },
    ]

    for d in data:
        b = BookModel(**d)
        db.session.add(b)

    db.session.commit()

    return app.test_client()