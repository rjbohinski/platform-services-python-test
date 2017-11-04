# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from handlers.rewards_handler import RewardsHandler
from handlers.order_handler import OrderHandler

url_patterns = [
    (r'/rewards/?', RewardsHandler),
    (r'/order/?', OrderHandler)
]
