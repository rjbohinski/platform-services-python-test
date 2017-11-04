# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import json
import tornado
from operator import itemgetter
from tornado import testing
from tornado.testing import AsyncHTTPClient


class TestRewardsHandler(tornado.testing.AsyncTestCase):
    """Tests the /rewards endpoint."""

    @tornado.testing.gen_test
    def test_rewards_accessible(self):
        """Call the '/rewards' endpoint to verify the web server is running"""
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:7050/rewards")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    def test_rewards_data(self):
        """Call the '/rewards' endpoint and test that the output.
        Verifies that the output can be parsed as JSON and the data matches
        the supplied test data.
        """
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:7050/rewards")
        self.assertEqual(response.code, 200)
        # Decode bytes into utf-8 string and parse the JSON
        data = json.loads(response.body.decode('utf-8'))
        # Sort the JSON output so we know the first tier is tier A,
        # at least based on the supplied test data.
        rewards = sorted(data, key=itemgetter("points"))
        self.assertEqual("A", rewards[0]["tier"])
        self.assertEqual(100, rewards[0]["points"])
        self.assertEqual("5% off purchase", rewards[0]["rewardName"])
