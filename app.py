from flask import jsonify, request, Response
from BookModel import *
from settings import *


def validBookObject(bookObject):
    if 'name' in bookObject and 'price' in bookObject and 'isbn' in bookObject:
        return True
    else:
        return False


# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


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
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
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
    return_value = Book.get_book(isbn)
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
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response


# PATCH /books/47566696346
# {
#     "name": "A",
# }
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if "name" in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if "price" in request_data:
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# DELETE /books/656684566987
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status=204)
        return response
    invalidBookObjectMSG = {
            "error": "Book with the ISBN number that was provided was not found, so therefore unable to delete"
        }
    response = Response(json.dumps(invalidBookObjectMSG), status=400, mimetype='application/json')
    return response


app.run(port=5000)
