# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import json
from operator import itemgetter
from urllib.parse import urlencode

import bson.json_util
import tornado
from tornado import testing
from tornado.testing import AsyncHTTPClient


class TestOrderHandler(tornado.testing.AsyncTestCase):
    """Tests the /order endpoint."""

    @tornado.testing.gen_test
    def test_order_accessible(self):
        """Call the '/order' endpoint to verify the web server is running"""
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:7050/order", method='POST',
                                      body=urlencode({
                                          'email_address': 'example@example.com',
                                          'order_total': 0.0}))
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    def test_order_error(self):
        """Call the '/order' endpoint and test that the output and database.
        Verifies that the output can be parsed as JSON.
        """
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:7050/order",
                                      method='POST',
                                      body=urlencode({}))
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertEqual("MissingArgumentError", data[0]["error"])
        self.assertEqual("MissingArgumentError", data[1]["error"])
        self.assertIn("' was not included in the message.", data[0]["detail"])
        self.assertIn("' was not included in the message.", data[1]["detail"])

    @tornado.testing.gen_test
    def test_order_data(self):
        """Call the '/order' endpoint and test that the output and database.
        Verifies that the output can be parsed as JSON.
        """
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(
            "http://localhost:7050/order",
            method='POST',
            body=urlencode({
                'email': 'example@example.com',
                'total': 100.80}))
        self.assertEqual(response.code, 200)
        # Decode bytes into utf-8 string and parse the JSON
        data = json.loads(response.body.decode('utf-8'))
        self.assertEqual(100, data["reward_points"])
        self.assertEqual("A", data["reward_tier"])
        self.assertEqual("5% off purchase", data["reward_tier_name"])
        self.assertEqual("10% off purchase", data["next_reward_tier_name"])
        self.assertEqual("B", data["next_reward_tier"])
        self.assertEqual(0.0, data["next_reward_tier_progress"])
        self.assertEqual("example@example.com", data["email_address"])

        response = yield client.fetch(
            "http://localhost:7050/order",
            method='POST',
            body=urlencode({
                'email': 'example@example.com',
                'total': 50}))
        self.assertEqual(response.code, 200)
        # Decode bytes into utf-8 string and parse the JSON
        data = json.loads(response.body.decode('utf-8'))
        self.assertEqual(150, data["reward_points"])
        self.assertEqual("A", data["reward_tier"])
        self.assertEqual("5% off purchase", data["reward_tier_name"])
        self.assertEqual("10% off purchase", data["next_reward_tier_name"])
        self.assertEqual("B", data["next_reward_tier"])
        self.assertEqual(0.5, data["next_reward_tier_progress"])
        self.assertEqual("example@example.com", data["email_address"])
