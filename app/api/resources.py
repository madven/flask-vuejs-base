import uuid
from datetime import datetime
from flask import request
from flask_restplus import Resource, reqparse, inputs, abort

from .security import require_auth
from . import api_rest


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True,
        'price': 19.99
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False,
        'price': 9.99
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True,
        'price': 3.99
    }
]


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]


@api_rest.route('/resource/<string:resource_id>')
class ResourceOne(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

    def post(self, resource_id):
        json_payload = request.json
        return {'timestamp': json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}


book_parser = reqparse.RequestParser()
book_parser.add_argument('title', type=str, required=True, location='json', help="Bu alan zorunludur.")
book_parser.add_argument('author', type=str, required=True, location='json', help="Bu alan zorunludur.")
book_parser.add_argument('read', type=inputs.boolean, required=True, location='json', help="Bu alan zorunludur.")
book_parser.add_argument('price', type=float, required=True, location='json', help="Bu alan zorunludur.")


@api_rest.route('/books')
class Books(Resource):

    def get(self):
        return {'books': BOOKS}

    def post(self):
        args = book_parser.parse_args()
        book = append_book(args)
        return book, 201


def abort_if_book_doesnt_exist(book_id):
    if not any(book['id'] == book_id for book in BOOKS):
        abort(404, message="Book {} doesn't exist".format(book_id))


@api_rest.route('/book/<string:id>')
class Book(Resource):

    def get(self, id):
        abort_if_book_doesnt_exist(id)
        book = next(book for book in BOOKS if book["id"] == id)
        return book

    def put(self, id):
        abort_if_book_doesnt_exist(id)
        args = book_parser.parse_args()
        remove_book(id)
        book = append_book(args)
        return book, 201

    def delete(self, id):
        abort_if_book_doesnt_exist(id)
        remove_book(id)
        return '', 204


def append_book(args):
    book = {
        'id': uuid.uuid4().hex,
        'title': args['title'],
        'author': args['author'],
        'read': args['read'],
        'price': args['price']
    }
    BOOKS.append(book)
    return book


def remove_book(book_id):
    BOOKS[:] = [book for book in BOOKS if book.get('id') != book_id]
