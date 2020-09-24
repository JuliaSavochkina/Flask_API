from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 656686987
    },
    {
        'name': 'Hello',
        'price': 7.99,
        'isbn': 656684566987
    },
    {
        'name': 'World',
        'price': 5.99,
        'isbn': 36656686987
    },
    {
        'name': 'The Cat in the Hat',
        'price': 6.99,
        'isbn': 4758596346
    }
]


def validBookObject(bookObject):
    if 'name' in bookObject and 'price' in bookObject and 'isbn' in bookObject:
        return True
    else:
        return False


# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})


# POST /books
# {
#         'name': 'F',
#         'price': 5.99,
#         'isbn': 47566696346
# }
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': '7.88', 'isbn': '123456789'"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


# GET /books/ISBN_NUMBER
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                "name": book['name'],
                "price": book['price']
            }
    return jsonify(return_value)


def valid_put_request_data(request_data):
    if 'name' in request_data and 'price' in request_data:
        return True
    else:
        return False


# PUT /books/47566696346
# {
#     "name": "A",
#     "price": 1.99
# }
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': '7.88'"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn = book['isbn']
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
        response = Response("", status=204)
    return response


# PATCH /books/47566696346
# {
#     "name": "A",
# }
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if "name" in request_data:
        updated_book["name"] = request_data["name"]
    if "price" in request_data:
        updated_book["price"] = request_data["price"]
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# DELETE /books/656684566987
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
        invalidBookObjectMSG = {
            "error": "Book with the ISBN number that was provided was not found, so therefore unable to delete"
        }
    response = Response(json.dump(invalidBookObjectMSG), status=400, mimetype='application/json')
    return response


app.run(port=5000)
