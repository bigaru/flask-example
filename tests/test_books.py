import json

#
# GetAll
#

def test_get_all_status_ok(app, client):
    res = client.get('/api/v1/books/')
    assert res.status_code == 200

def test_get_all_content(app, client):
    res = client.get('/api/v1/books/')

    assert res.get_json() == [
        { "isbn":"978-3840024634", "name": "Foo Master", "price": 9.99 },
        { "isbn":"878-3840024634", "name": "Bar", "price": 9.99 },
        { "isbn":"778-3840024634", "name": "Planer", "price": 9.99 }
    ]

#
# Get
#

def test_get_status_ok(app, client):
    res = client.get('/api/v1/books/978-3840024634')
    assert res.status_code == 200

def test_get_content(app, client):
    res = client.get('/api/v1/books/978-3840024634')
    assert res.get_json() == { "isbn":"978-3840024634", "name": "Foo Master", "price": 9.99 }

def test_get_status_not_found(app, client):
    res = client.get('/api/v1/books/078-3840024634')
    assert res.status_code == 404

def test_get_content_not_found(app, client):
    res = client.get('/api/v1/books/078-3840024634')
    assert res.get_json() == { "message": "item not found" }


#
# Create
#

def test_create_status_created(app, client):
    data = { "isbn":"678-3840024634", "name": "Foo Master", "price": 9.99 }
    res = client.post('/api/v1/books/', json=data)
    assert res.status_code == 201

def test_create_content(app, client):
    data = { "isbn":"678-3840024631", "name": "Foo Master", "price": 9.99 }
    res = client.post('/api/v1/books/', json=data)
    assert res.get_json() == { "isbn":"678-3840024631", "name": "Foo Master", "price": 9.99 }

def test_create_missing_field_status(app, client):
    data = { "isbn":"678-3840024634", "price": 9.99 }
    res = client.post('/api/v1/books/', json=data)
    assert res.status_code == 400

def test_create_missing_field_content(app, client):
    data = { "isbn":"678-3840024634", "price": 9.99 }
    res = client.post('/api/v1/books/', json=data)
    assert res.json == {'name': ['Missing data for required field.']}

def test_create_isbn_exists_already_status(app, client):
    data = { "isbn":"978-3840024634", "name": "Foo Master", "price": 9.99 }
    res = client.post('/api/v1/books/', json=data)
    assert res.status_code == 400

def test_create_isbn_exists_already_content(app, client):
    data = { "isbn":"978-3840024634", "name": "Foo Master", "price": 9.99 }
    res = client.post('/api/v1/books/', json=data)
    assert res.json == {'message': 'isbn exists already'}

#
# Update
#

def test_update_status_created(app, client):
    data = { "isbn":"578-3840024634", "name": "Foo Master", "price": 9.99 }
    res = client.put('/api/v1/books/578-3840024634', json=data)
    assert res.status_code == 200

def test_update_content_created(app, client):
    data = { "isbn":"568-3840024631", "name": "Foo Master", "price": 9.99 }
    res = client.put('/api/v1/books/568-3840024631', json=data)
    assert res.get_json() == { "isbn":"568-3840024631", "name": "Foo Master", "price": 9.99 }

def test_update_missing_field_status(app, client):
    data = { "isbn":"578-3840024634", "price": 9.99 }
    res = client.put('/api/v1/books/578-3840024634', json=data)
    assert res.status_code == 400

def test_update_missing_field_content(app, client):
    data = { "isbn":"578-3840024634", "price": 9.99 }
    res = client.put('/api/v1/books/578-3840024634', json=data)
    assert res.json == {'name': ['Missing data for required field.']}

def test_update_status(app, client):
    data = { "isbn":"978-3840024634", "name": "Boo Master", "price": 9.99 }
    res = client.put('/api/v1/books/978-3840024634', json=data)
    assert res.status_code == 200

def test_update_content(app, client):
    data = { "isbn":"978-3840024631", "name": "Boo", "price": 7.99 }
    res = client.put('/api/v1/books/978-3840024631', json=data)
    assert res.get_json() == { "isbn":"978-3840024631", "name": "Boo", "price": 7.99 }

def test_update_id_not_match_status(app, client):
    data = { "isbn":"6", "name": "Boo Master", "price": 9.99 }
    res = client.put('/api/v1/books/4', json=data)
    assert res.status_code == 400

def test_update_id_not_match_content(app, client):
    data = { "isbn":"5", "name": "Boo", "price": 7.99 }
    res = client.put('/api/v1/books/4', json=data)
    assert res.get_json() == {  "message": "isbn did not match" }

#
# Delete
#

def test_delete(app, client):
    res = client.delete('/api/v1/books/778-3840024634')
    assert res.status_code == 200
    assert res.json == { "message": "deleted successfully" }

def test_delete_not_found(app, client):
    res = client.delete('/api/v1/books/3840024634')
    assert res.status_code == 404
    assert res.json == { "message": "item not found" }