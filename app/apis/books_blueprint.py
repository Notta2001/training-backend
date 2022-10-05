import uuid

from sanic import Blueprint
from sanic.response import json

from app.decorators.auth import protected
from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiBadRequest, ApiForbidden
from app.hooks.error import ApiInternalError
from app.models.book import create_book_json_schema, update_book_json_schema, Book

books_bp = Blueprint('books_blueprint', url_prefix='/books')

_db = MongoDB()


@books_bp.route('/')
async def get_all_books(request):
    # # TODO: use cache to optimize api
    async with request.app.ctx.redis as r:
        books = await get_cache(r, CacheConstants.all_books)
        if books is None:
            book_objs = _db.get_books()
            books = [book.to_dict() for book in book_objs]
            await set_cache(r, CacheConstants.all_books, books)

    book_objs = _db.get_books()
    books = [book.to_dict() for book in book_objs]
    number_of_books = len(books)
    return json({
        'n_books': number_of_books,
        'books': books
    })


@books_bp.route('/', methods={'POST'})
@protected  # TODO: Authenticate
@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def create_book(request, username=None):
    body = request.json

    book_id = str(uuid.uuid4())
    book = Book(book_id).from_dict(body)
    book.owner = username

    # TODO: Save book to database
    inserted = _db.create_book(book)
    if not inserted:
        raise ApiInternalError('Fail to create book')

    # TODO: Update cache

    return json({'status': 'success'})


# TODO: write api get, update, delete book
# Get book
@books_bp.route('/<_id>', methods=['GET'])
async def read_book(request, _id: uuid.UUID):
    book_obj = _db.get_book_by_id(_id)
    print(book_obj)
    if not book_obj:
        raise ApiBadRequest('Book: Not found!')
    else:
        book = book_obj.to_dict()
    return json({
        'status': 'success',
        'created_book': book
    })

# Update book
@books_bp.route('/<_id>', methods=['PUT'])
@protected
@validate_with_jsonschema(update_book_json_schema)
async def update_book(request, _id: uuid.UUID, username=None):
    body = request.json

    book_obj = _db.get_book_by_id(_id)
    if not book_obj:
        raise ApiBadRequest('Book: Not found!')

    if not (book_obj.owner == username):
        raise ApiForbidden('You dont have the right to update book!')
    
    updated_book_obj = _db.update_book(_id, set_doc=body)
    if not updated_book_obj:
        raise ApiBadRequest("Book: Fail to update!")
    else:
        updated_book = updated_book_obj.to_dict()
        return json({
            'status': 'success',
            'updated book': updated_book
        })
    
# Delete book
@books_bp.route('/<_id>', methods=['DELETE'])
@protected
async def delete_book(request, _id: uuid.UUID, username=None):
    book_obj = _db.get_book_by_id(_id)
    if not book_obj:
        raise ApiBadRequest('Book: Not found!')

    if not (book_obj.owner == username):
        raise ApiForbidden('You dont have the right to delete book!')
    
    deleted_book_obj = _db.delete_book(_id)
    if not deleted_book_obj:
        raise ApiBadRequest('Book: Failt to delete!')
    else:
        return json({
            'status': 'success',
            'deleted book': book_obj.to_dict()
        })