# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import bson.json_util
import tornado.web
from tornado.gen import coroutine
import logging
from db.customers import Customers



class OrderHandler(tornado.web.RequestHandler):
    """Handler for the '/order' endpoint."""

    logger = logging.getLogger("OrderHandler")

    @coroutine
    def post(self):
        """On a post call, either add or update a customer record.
        Requires the arguments 'email' and 'total'.
        """
        OrderHandler.logger.debug("OrderHandler.post()")
        email = self.get_argument("email")
        total = self.get_argument("total")
        OrderHandler.logger.debug("Email: %s, Total: %s", email, total)

        customer = Customers.auto_insert_update(email, total)
        OrderHandler.logger.debug("Customer: %s", customer)

        self.write(bson.json_util.dumps(customer))
        # self.write()
