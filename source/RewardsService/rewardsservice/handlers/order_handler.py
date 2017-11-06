# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import json
import logging

import bson.json_util
import tornado.web
from tornado.gen import coroutine
from tornado.web import MissingArgumentError

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

        # Verify that the required arguments were provided.
        error_data = []
        try:
            email = self.get_argument("email")
        except MissingArgumentError:
            error_data.append(
                {"error": "MissingArgumentError",
                 "detail": "The argument 'email' was not included in the message."})
        try:
            total = self.get_argument("total")
        except MissingArgumentError:
            error_data.append(
                {"error": "MissingArgumentError",
                 "detail": "The argument 'total' was not included in the message."})

        # If there were any errors, return the error message.
        if error_data is not None and len(error_data) is not 0:
            self.write(json.dumps(error_data))
        else:
            OrderHandler.logger.debug("Email: %s, Total: %s", email, total)

            customer = Customers.auto_insert_update(email, total)
            OrderHandler.logger.debug("Customer: %s", customer)

            self.write(bson.json_util.dumps(customer))
