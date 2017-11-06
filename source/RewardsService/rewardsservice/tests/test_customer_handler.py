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


class TestCustomerHandler(tornado.testing.AsyncTestCase):
    """Tests the /customer endpoint."""

    @tornado.testing.gen_test
    def test_customer_accessible(self):
        """Call the '/customer' endpoint to verify the web server is running"""
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:7050/customer", method='POST',
                                      body=urlencode({
                                          'email_address': 'example-customer@example.com'}))
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    def test_customer_not_exist(self):
        """Call the '/customer' endpoint and test that the output and database.
        Verifies that the output can be parsed as JSON.
        """
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:7050/customer",
                                      method='POST',
                                      body=urlencode({'email': 'example-not-found@example.com'}))
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertEqual("CustomerNotFoundError", data[0]["error"])
        self.assertIn(
            "The customer with email 'example-not-found@example.com' was not found in the database.",
            data[0]["detail"])

    @tornado.testing.gen_test
    def test_customer_data(self):
        """Call the '/customer' endpoint and test that the output and database.
        Verifies that the output can be parsed as JSON.
        """
        client = AsyncHTTPClient(self.io_loop)

        # First load the database with sample orders to ensure the customer
        # exists.
        response = yield client.fetch(
            "http://localhost:7050/order",
            method='POST',
            body=urlencode({
                'email': 'example-customer@example.com',
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
        self.assertEqual("example-customer@example.com", data["email_address"])

        response = yield client.fetch(
            "http://localhost:7050/order",
            method='POST',
            body=urlencode({
                'email': 'example-customer@example.com',
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
        self.assertEqual("example-customer@example.com", data["email_address"])

        # Call the customer endpoint to verify
        response = yield client.fetch(
            "http://localhost:7050/customer",
            method='POST',
            body=urlencode({
                'email': 'example-customer@example.com'}))
        self.assertEqual(response.code, 200)
        # Decode bytes into utf-8 string and parse the JSON
        data = json.loads(response.body.decode('utf-8'))
        print("Data: {}".format(data))
        self.assertEqual(150, data["reward_points"])
        self.assertEqual("A", data["reward_tier"])
        self.assertEqual("5% off purchase", data["reward_tier_name"])
        self.assertEqual("10% off purchase", data["next_reward_tier_name"])
        self.assertEqual("B", data["next_reward_tier"])
        self.assertEqual(0.5, data["next_reward_tier_progress"])
        self.assertEqual("example-customer@example.com", data["email_address"])
