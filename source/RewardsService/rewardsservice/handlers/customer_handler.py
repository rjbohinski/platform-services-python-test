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


class CustomerHandler(tornado.web.RequestHandler):
    """Handler for the '/customer' endpoint."""

    logger = logging.getLogger("CustomerHandler")

    @coroutine
    def post(self):
        """On a post call, retrieve a customer record.
        Requires the arguments 'email'.
        """
        CustomerHandler.logger.debug("CustomerHandler.post()")

        # Verify that the required arguments were provided.
        error_data = []
        try:
            email = self.get_argument("email")
        except MissingArgumentError:
            error_data.append(
                {"error": "MissingArgumentError",
                 "detail": "The argument 'email' was not included in the message."})

        # If there were any errors, return the error message.
        if error_data is not None and len(error_data) is not 0:
            self.write(json.dumps(error_data))
        else:
            CustomerHandler.logger.debug("Email: %s", email)

            customer = Customers.get(email)
            CustomerHandler.logger.debug("Customer: %s", customer)

            if customer is None:
                error_data.append(
                    {"error": "CustomerNotFoundError",
                     "detail": "The customer with email '{}' was not found in the database.".format(
                         email)})

            if error_data is not None and len(error_data) is not 0:
                self.write(json.dumps(error_data))
            else:
                self.write(bson.json_util.dumps(customer))
