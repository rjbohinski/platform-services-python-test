# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from pymongo import MongoClient


class MongoDBManager(object):
    DEFAULT_DB_HOST = "mongodb"
    DEFAULT_DB_PORT = 27017

    def __init__(self, host=DEFAULT_DB_HOST, port=DEFAULT_DB_PORT):
        try:
            # Python 2
            if not isinstance(host, (unicode, str)):
                raise TypeError('host is not of type unicode or str.')
        except NameError:
            # Python 3
            if not isinstance(host, str):
                raise TypeError('host is not of type str.')
        if not isinstance(port, int):
            try:
                port = int(port)
            except ValueError:
                raise TypeError('port is not of type int.')

        self.host = host
        self.port = port
        self.client = None

    def get_client(self):
        if self.client is None:
            self.client = MongoClient(self.host, self.port)
        return self.client
