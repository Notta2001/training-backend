import re
from turtle import update
from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections
from app.models.book import Book
from app.models.user import User
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            connection_url = f'mongodb://{MongoDBConfig.USERNAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}'

        self.connection_url = connection_url.split('@')[-1]
        self.client = MongoClient(connection_url)
        self.db = self.client[MongoDBConfig.DATABASE]

        self._books_col = self.db[MongoCollections.books]
        self._users_col = self.db[MongoCollections.users]

    def get_books(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._books_col.find(filter_, projection=projection)
            data = []
            for doc in cursor:
                data.append(Book().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []
    
    def get_book_by_id(self, _id):
        try:
            filter_ = {'_id': str(_id)}
            print(filter_)
            doc = self._books_col.find_one(filter_)
            if doc:
                data = Book().from_dict(doc)
                return data
        except Exception as ex:
            logger.exception(ex)
        return []

    def create_book(self, book: Book):
        try:
            insert_doc = self._books_col.insert_one(book.to_dict())
            return insert_doc
        except Exception as ex:
            logger.exception(ex)
        return []
    
    def update_book(self, _id, set_doc=None):
        try:
            if not set_doc:
                return None
            filter_ = {'_id': str(_id)}
            query_ = {'$set': set_doc}
            modified_doc = self._books_col.update_one(filter_, query_)
            if modified_doc.modified_count:
                updated_doc = self._books_col.find_one(filter_)
                updated_book = Book().from_dict(updated_doc)
                return updated_book
        except Exception as ex:
            logger.exception(ex)
        return None
    
    def delete_book(self, _id):
        try: 
            filter_ = {'_id': str(_id)}
            deleted_doc = self._books_col.delete_one(filter_)
            if deleted_doc.deleted_count:
                return True
        except Exception as ex:
            logger.exception(ex)
        return None
        
    def get_users(self, filter_=None, projection=None):
        try: 
            if not filter_:
                filter_ = {}
            cursor: self._users_col.find(filter_, projection=projection)
            data = []
            for doc in cursor:
                data.append(User().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []

    def get_user_by_username(self, username: str):
        try:
            filter_ = {'username': username}
            doc = self._users_col.find_one(filter_)
            if doc:
                data = User().from_dict(doc)
                return data
        except Exception as ex:
            logger.exception(ex)
        return []

    def create_user(self, user: User):
        try:
            insert_doc = self._users_col.insert_one(user.to_dict())
            return insert_doc
        except Exception as ex:
            logger.exception(ex)
        return []

    # def add_book(self, book: Book):
    #     try:
    #         inserted_doc = self._books_col.insert_one(book.to_dict())
    #         return inserted_doc
    #     except Exception as ex:
    #         logger.exception(ex)
    #     return None

    # TODO: write functions CRUD with books
