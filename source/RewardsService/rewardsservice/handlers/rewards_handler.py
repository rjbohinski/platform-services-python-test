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

    @coroutine
    def get(self):
        client = MongoDBManager().get_client()
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
