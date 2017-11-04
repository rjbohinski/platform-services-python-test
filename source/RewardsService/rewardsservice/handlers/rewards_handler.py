# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import json

import tornado.web
from tornado.gen import coroutine

from db.mongodb_manager import MongoDBManager


class RewardsHandler(tornado.web.RequestHandler):
    """Handler for the '/rewards' endpoint."""

    @coroutine
    def get(self):
        """On a get call, return all rewards data in a JSON format."""
        client = MongoDBManager().get_client()
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
