import unittest
import os

from app import app

from mockupdb import MockupDB, go, Command
from pymongo import MongoClient
#from json import dumps

class GetDataSourceTestCase(unittest.TestCase):

    def test_getDataSource(self):
        # arrange
        id = 1
        future = go(self.app.get, f'/add_icecream_id/{id}')
        request = self.server.receives(
            Command({'find': 'dataSources', 'filter': {'_id': id}, 'limit': 1, 'singleBatch': True}, flags=4, namespace='app'))
        request.ok(cursor={'id': 0, 'firstBatch': [
            { "icecream_name" : "Rassberry", "icecream_flavour" : "Rassberry", "Icecream_type" : "Bar", "Icecream_price" : "30/-", "description" : "Nice"  }]})

        # act
        http_response = future()
        # assert
        self.assertIn('http://google.com/rest/api',http_response.get_data(as_text=True))
