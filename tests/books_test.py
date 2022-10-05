from urllib import response
from main import app
import json
import unittest

class BooksTests(unittest.TestCase):
    """ Unit testcases for REST APIs """

    def test_get_all_books(self):
        request, response = app.test_client.get('/books')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_books'), 0)
        self.assertIsInstance(data.get('books'), list)

    # def test_login(self):
    #     request, response = app.test_client.post('/users/login', data=dict(username= "admin",password= "admin123"))
    #     print(response)
    #     data = json.loads(response.text)
    #     self.assertEqual(data.get('username'), 'admin')

    def test_read_books(self):
        book = {
            "_id": "6d3fa486-22e8-4957-9c08-08ba9b3a2677",
            "title": "Gone with the Wind",
            "authors": [
                "Margaret Mitchell"
            ],
            "publisher": "Times",
            "description": "What books, do you think, suit the saying: Those were the good old days!(with a dramatic ohhhh!). List your favorite good old poetry, good old fairytales—anything good, but OLD.",
            "owner": "doanthang2001",
            "createdAt": 1664955111,
            "lastUpdatedAt": 1664955111
        }
        request, response = app.test_client.get('/books/6d3fa486-22e8-4957-9c08-08ba9b3a2677')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data.get('created_book'), book)
    
    # def test_delete_book(self):
    #     book = {
    #         "_id": "6d3fa486-22e8-4957-9c08-08ba9b3a2677",
    #         "title": "Gone with the Wind",
    #         "authors": [
    #             "Margaret Mitchell"
    #         ],
    #         "publisher": "Times",
    #         "description": "What books, do you think, suit the saying: Those were the good old days!(with a dramatic ohhhh!). List your favorite good old poetry, good old fairytales—anything good, but OLD.",
    #         "owner": "doanthang2001",
    #         "createdAt": 1664955111,
    #         "lastUpdatedAt": 1664955111
    #     }
    #     request, response = app.test_client.delete('/books/6d3fa486-22e8-4957-9c08-08ba9b3a2677')
    #     self.assertEqual(response.status, 200)
    #     data = json.loads(response.text)
    #     self.assertEqual(data.get('deleted_book'), book)
        

    # TODO: unittest for another apis

if __name__ == '__main__':
    unittest.main()
